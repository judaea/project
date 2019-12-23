# -*- coding: utf-8 -*-

import json
import re
import requests
import time
import threading

from resources.lib.modules import source_utils
from resources.lib.modules import control
from resources.lib.modules import database


class RealDebrid:
    def __init__(self):
        self.ClientID = control.getSetting('rd.client_id')
        if self.ClientID == '':
            self.ClientID = 'X245A4XAIBGVM'
        self.OauthUrl = 'https://api.real-debrid.com/oauth/v2/'
        self.DeviceCodeUrl = "device/code?%s"
        self.DeviceCredUrl = "device/credentials?%s"
        self.TokenUrl = "token"
        self.token = control.getSetting('rd.auth')
        self.refresh = control.getSetting('rd.refresh')
        self.DeviceCode = ''
        self.ClientSecret = control.getSetting('rd.secret')
        self.OauthTimeout = 0
        self.OauthTimeStep = 0
        self.BaseUrl = "https://api.real-debrid.com/rest/1.0/"
        self.cache_check_results = {}

    def auth_loop(self):
        if control.progressDialog.iscanceled():
            control.progressDialog.close()
            return
        time.sleep(self.OauthTimeStep)
        url = "client_id=%s&code=%s" % (self.ClientID, self.DeviceCode)
        url = self.OauthUrl + self.DeviceCredUrl % url
        response = json.loads(requests.get(url).text)
        if 'error' in response:
            return
        else:
            try:
                control.progressDialog.close()
                control.setSetting('rd.client_id', response['client_id'])
                control.setSetting('rd.secret', response['client_secret'])
                self.ClientSecret = response['client_secret']
                self.ClientID = response['client_id']
            except:
                control.showDialog.ok(control.addonName, control.lang(32100))
            return

    def auth(self):
        self.ClientSecret = ''
        self.ClientID = 'X245A4XAIBGVM'
        url = ("client_id=%s&new_credentials=yes" % self.ClientID)
        url = self.OauthUrl + self.DeviceCodeUrl % url
        response = json.loads(requests.get(url).text)
        control.copy2clip(response['user_code'])
        control.progressDialog.create(control.lang(32023))
        control.progressDialog.update(-1, control.lang(32024).format(control.colorString(
            'https://real-debrid.com/device')),
                                    control.lang(32025).format(control.colorString(
                                        response['user_code'])),
                                    'This code has been copied to your clipboard')
        self.OauthTimeout = int(response['expires_in'])
        self.OauthTimeStep = int(response['interval'])
        self.DeviceCode = response['device_code']

        while self.ClientSecret == '':
            self.auth_loop()

        self.token_request()

        user_information = self.get_url('user')
        if user_information['type'] != 'premium':
            control.showDialog.ok(control.addonName, control.lang(40156))

    def token_request(self):
        import time
        if self.ClientSecret is '':
            return

        postData = {'client_id': self.ClientID,
                    'client_secret': self.ClientSecret,
                    'code': self.DeviceCode,
                    'grant_type': 'http://oauth.net/grant_type/device/1.0'}

        url = self.OauthUrl + self.TokenUrl
        response = requests.post(url, data=postData).text
        response = json.loads(response)
        control.setSetting('rd.auth', response['access_token'])
        control.setSetting('rd.refresh', response['refresh_token'])
        self.token = response['access_token']
        self.refresh = response['refresh_token']
        control.setSetting('rd.expiry', str(time.time() + int(response['expires_in'])))
        username = self.get_url('user')['username']
        control.setSetting('rd.username', username)
        control.showDialog.ok(control.addonName, 'Real Debrid ' + control.lang(32026))
        control.log('Authorised Real Debrid successfully', 'info')

    def refreshToken(self):
        import time
        postData = {'grant_type': 'http://oauth.net/grant_type/device/1.0',
                    'code': self.refresh,
                    'client_secret': self.ClientSecret,
                    'client_id': self.ClientID
                    }
        url = self.OauthUrl + 'token'
        response = requests.post(url, data=postData)
        response = json.loads(response.text)
        if 'access_token' in response:
            self.token = response['access_token']
        else:
            pass
        if 'refresh_token' in response:
            self.refresh = response['refresh_token']
        control.setSetting('rd.auth', self.token)
        control.setSetting('rd.refresh', self.refresh)
        control.setSetting('rd.expiry', str(time.time() + int(response['expires_in'])))
        control.log('Real Debrid Token Refreshed')
        ###############################################
        # To be FINISHED FINISH ME
        ###############################################

    def post_url(self, url, postData, fail_check=False):
        original_url = url
        url = self.BaseUrl + url
        if self.token == '':
            return None
        if not fail_check:
            if '?' not in url:
                url += "?auth_token=%s" % self.token
            else:
                url += "&auth_token=%s" % self.token

        response = requests.post(url, data=postData, timeout=5).text
        if 'bad_token' in response or 'Bad Request' in response:
            if not fail_check:
                self.refreshToken()
                response = self.post_url(original_url, postData, fail_check=True)
        try:
            return json.loads(response)
        except:
            return response

    def get_url(self, url, fail_check=False):
        original_url = url
        url = self.BaseUrl + url
        if self.token == '':
            control.log('No Real Debrid Token Found')
            return None
        if not fail_check:
            if '?' not in url:
                url += "?auth_token=%s" % self.token
            else:
                url += "&auth_token=%s" % self.token

        response = requests.get(url, timeout=5).text

        if 'bad_token' in response or 'Bad Request' in response:
            control.log('Refreshing RD Token')
            if not fail_check:
                self.refreshToken()
                response = self.get_url(original_url, fail_check=True)
        try:
            return json.loads(response)
        except:
            return response

    def checkHash(self, hashList):

        if isinstance(hashList, list):
            cache_result = {}
            hashList = [hashList[x:x+100] for x in range(0, len(hashList), 100)]
            threads = []
            for section in hashList:
                threads.append(threading.Thread(target=self._check_hash_thread, args=(section,)))
            for i in threads:
                i.start()
            for i in threads:
                i.join()
            return self.cache_check_results
        else:
            hashString = "/" + hashList
            return self.get_url("torrents/instantAvailability" + hashString)

    def _check_hash_thread(self, hashes):
        hashString = '/' + '/'.join(hashes)
        response = self.get_url("torrents/instantAvailability" + hashString)
        self.cache_check_results.update(response)

    def addMagnet(self, magnet):
        postData = {'magnet': magnet}
        url = 'torrents/addMagnet'
        response = self.post_url(url, postData)
        return response

    def list_torrents(self):
        url = "torrents"
        response = self.get_url(url)
        return response

    def torrentInfo(self, id):
        url = "torrents/info/%s" % id
        return self.get_url(url)

    def torrentSelect(self, torrentID, fileID):
        url = "torrents/selectFiles/%s" % torrentID
        postData = {'files': fileID}
        return self.post_url(url, postData)

    def resolve_hoster(self, link):
        url = 'unrestrict/link'
        postData = {'link': link}
        response = self.post_url(url, postData)
        try:
            return response['download']
        except:
            return None

    def deleteTorrent(self, id):
        if self.token == '':
            return None
        url = "torrents/delete/%s&auth_token=%s" % (id, self.token)
        requests.delete(self.BaseUrl + url, timeout=5)

    def _single_magnet_resolve(self, torrent):
        try:
            magnet = torrent['magnet']

            try:
                hash = str(re.findall(r'btih:(.*?)(?:&|$)', magnet)[0].lower())
            except:
                hash = torrent['hash']

            hashCheck = self.checkHash(hash)

            fileIDString = ''

            if hash in hashCheck:
                if 'rd' in hashCheck[hash]:
                    for key in hashCheck[hash]['rd'][0]:
                        fileIDString += ',' + key

            torrent = self.addMagnet(magnet)
            try:
                self.torrentSelect(torrent['id'], fileIDString[1:])
                link = self.torrentInfo(torrent['id'])
                selected_files = [i for i in link['files'] if i['selected'] == 1]
                if len(selected_files) == 1:
                    link_index = 0
                else:
                    link_index = 0
                    index_bytes = 0
                    for idx, file in enumerate(selected_files):
                        if file['bytes'] > index_bytes:
                            link_index = idx
                link = self.resolve_hoster(link['links'][link_index])
                if control.getSetting('rd.autodelete') == 'true':
                    self.deleteTorrent(torrent['id'])
            except:
                import traceback
                traceback.print_exc()
                self.deleteTorrent(torrent['id'])
                return None
            return link
        except:
            import traceback
            traceback.print_exc()
            return None

    def resolve_magnet(self, magnet, args, torrent, pack_select=False):
        try:
            if torrent['package'] == 'single' or 'showInfo' not in args:
                return self._single_magnet_resolve(torrent)

            try:
                hash = str(re.findall(r'btih:(.*?)(?:&|$)', torrent['magnet'])[0].lower())
            except:
                hash = torrent['hash']

            hashCheck = self.checkHash(hash)
            torrent = self.addMagnet(torrent['magnet'])
            episodeStrings, seasonStrings = source_utils.torrentCacheStrings(args)
            key_list = []

            for storage_variant in hashCheck[hash]['rd']:
                file_inside = False
                key_list = []
                bad_storage = False

                for key, value in storage_variant.items():
                    file_name = storage_variant[key]['filename']

                    if not any(file_name.endswith(extension) for extension in
                               source_utils.COMMON_VIDEO_EXTENSIONS):
                        bad_storage = True
                        break

                    else:
                        file_name = file_name.replace(source_utils.get_quality(file_name), '')
                        file_name = source_utils.cleanTitle(file_name)
                        key_list.append(key)
                        if any(episodeString in source_utils.cleanTitle(file_name) for
                               episodeString in episodeStrings):
                            file_inside = True

                if not file_inside or bad_storage:
                    continue
                else:
                    break

            if len(key_list) == 0:
                self.deleteTorrent(torrent['id'])
                return None

            key_list = ','.join(key_list)

            self.torrentSelect(torrent['id'], key_list)

            link = self.torrentInfo(torrent['id'])

            file_index = None

            for idx, i in enumerate([i for i in link['files'] if i['selected'] == 1]):
                file_name = i['path'].split('/')[-1]
                file_name = file_name.replace(source_utils.get_quality(file_name), '')
                file_name = source_utils.cleanTitle(file_name)

                if any(source_utils.cleanTitle(episodeString) in file_name for
                       episodeString in episodeStrings):
                        file_index = idx
                        break

            if file_index is None:
                self.deleteTorrent(torrent['id'])
                return None

            link = link['links'][file_index]
            link = self.resolve_hoster(link)

            if link.endswith('rar'):
                link = None

            if control.getSetting('rd.autodelete') == 'true':
                self.deleteTorrent(torrent['id'])
            return link
        except:
            import traceback
            traceback.print_exc()
            self.deleteTorrent(torrent['id'])
            return None

    def getRelevantHosters(self):
        try:
            host_list = self.get_url('hosts/status')
            valid_hosts = []
            try:
                for domain, status in host_list.iteritems():
                    if status['supported'] == 1 and status['status'] == 'up':
                        valid_hosts.append(domain)
            except:
                # Python 3 support
                for domain, status in host_list.items():
                    if status['supported'] == 1 and status['status'] == 'up':
                        valid_hosts.append(domain)
            return valid_hosts
        except:
            import traceback
            traceback.print_exc()

    def get_hosters(self, hosters):
        host_list = database.get(self.getRelevantHosters, 1)
        if host_list is None:
            host_list = self.getRelevantHosters()
        if host_list is not None:
            hosters['premium']['real_debrid'] = [(i, i.split('.')[0]) for i in host_list]
        else:
            hosters['premium']['real_debrid'] = []