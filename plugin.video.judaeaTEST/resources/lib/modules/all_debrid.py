# -*- coding: utf-8 -*-

import requests
import time

from resources.lib.modules import control
from resources.lib.modules import database
from resources.lib.modules import source_utils

class AllDebrid:

    def __init__(self):
        self.agent_identifier = control.addonName
        self.token = control.getSetting('alldebrid.token')
        self.base_url = 'https://api.alldebrid.com/'

    def get_url(self, url, token_req=False):

        if not control.getSetting('alldebrid.enabled') == 'true' or self.token == '':
            return

        url = '{}{}'.format(self.base_url, url)

        if not '?' in url:
            url += '?'
            url += 'agent={}'.format(self.agent_identifier)
        else:
            url += '&agent={}'.format(self.agent_identifier)

        if token_req:
            url += '&token={}'.format(self.token)

        return requests.get(url).json()

    def post_url(self, url, post_data=None, token_req=False):

        if not control.getSetting('alldebrid.enabled') == 'true' or self.token == '':
            return

        url = '{}{}'.format(self.base_url, url)

        if not '?' in url:
            url += '?'
            url += 'agent={}'.format(self.agent_identifier)
        else:
            url += '&agent={}'.format(self.agent_identifier)

        if token_req:
            url += '&token={}'.format(self.token)

        return requests.post(url, data=post_data).json()

    def auth(self):
        pin_url = '{}/pin/get?agent={}'.format(self.base_url, self.agent_identifier)
        resp = requests.get(pin_url).json()

        expiry = pin_ttl = int(resp['expired_in'])
        auth_complete = False
        control.copy2clip(resp['pin'])

        control.progressDialog.create('{} - {}'.format(control.addonName, 'AllDebrid Auth'))
        control.progressDialog.update(100, control.lang(32024).format(control.colorString(resp['base_url'])),
                                    control.lang(32025).format(control.colorString(
                                        resp['pin'])),
                                    'This code has been copied to your clipboard')

        # Seems the All Debrid servers need some time do something with the pin before polling
        # Polling to early will cause an invalid pin error
        time.sleep(5)

        while not auth_complete and not expiry <= 0 and not control.progressDialog.iscanceled():

            auth_complete, expiry = self.poll_auth(resp['check_url'])
            progress_percent = 100 - int((float(pin_ttl - expiry) / pin_ttl) * 100)
            control.progressDialog.update(progress_percent)
            time.sleep(1)

        try:control.progressDialog.close()
        except:pass

        self.store_user_info()

        if auth_complete:
            control.showDialog.ok(control.addonName, 'AllDebrid {}'.format(control.lang(32026)))
        else:
            return

    def poll_auth(self, poll_url):

        resp = requests.get(poll_url).json()
        if resp['activated']:
            control.setSetting('alldebrid.token', resp['token'])
            self.token = resp['token']
            return True, 0

        return False, int(resp['expires_in'])


    def store_user_info(self):
        user_information = self.get_url('user/login', True)
        control.setSetting('alldebrid.username', user_information['user']['username'])
        return

    def check_hash(self, hash_list):

        post_data = {'magnets[]': hash_list}

        return self.post_url('magnet/instant', post_data, True)

    def upload_magnet(self, hash):
        return self.get_url('magnet/upload?magnet={}'.format(hash), token_req=True)

    def update_relevant_hosters(self):
        return self.get_url('hosts')

    def get_hosters(self, hosters):

        host_list = database.get(self.update_relevant_hosters, 1)
        if host_list is None:
            host_list = self.update_relevant_hosters()
        if host_list is not None:
            hosters['premium']['all_debrid'] = [(i['domain'], i['domain'].split('.')[0])
                                                for i in host_list['hosts'] if i['status']]
            hosters['premium']['all_debrid'] += [(host, host.split('.')[0])
                                                for i in host_list['hosts'] if 'altDomains' in i and i['status']
                                                for host in i['altDomains']]
        else:
            import traceback
            traceback.print_exc()
            hosters['premium']['all_debrid'] = []

    def resolve_hoster(self, url):
        url = control.quote(url)
        resolve = self.get_url('link/unlock?link={}'.format(url), token_req=True)
        if resolve['success']:
            return resolve['infos']['link']
        else:
            return None

    def magnet_status(self, magnet_id):
        return self.get_url('magnet/status?id={}'.format(magnet_id), token_req=True)

    def movie_magnet_to_stream(self, magnet, args):
        selectedFile = None

        magnet_id = self.upload_magnet(magnet)['id']
        folder_details = self.magnet_status(magnet_id)['links']

        folder_details = [(key, value) for key, value in folder_details.iteritems()
                          if any(value.endswith(ext) for ext in source_utils.COMMON_VIDEO_EXTENSIONS)]

        for torrent_file in folder_details:
            if source_utils.filter_movie_title(torrent_file[1],
                                               control.deaccentString(args['info']['title']),
                                               args['info']['year']):
                selectedFile = torrent_file[0]
                break

        if selectedFile is None:
            folder_details = [tfile for tfile in folder_details if 'sample' not in tfile[1].lower()]
            folder_details = [tfile for tfile in folder_details if source_utils.cleanTitle(args['info']['title'])
                              in source_utils.cleanTitle(tfile[1].lower())]
            if len(folder_details) == 1:
                selectedFile = folder_details[0]
            else:
                return

        return self.resolve_hoster(selectedFile)

    def resolve_magnet(self, magnet, args, torrent, pack_select=False):

        if 'showInfo' not in args:
            return self.movie_magnet_to_stream(magnet, args)

        magnet_id = self.upload_magnet(magnet)
        magnet_id = magnet_id['id']

        episodeStrings, seasonStrings = source_utils.torrentCacheStrings(args)

        try:
            folder_details = self.magnet_status(magnet_id)

            if folder_details['status'] != 'Ready':
                return

            folder_details = [{'link': key, 'filename': value} for key, value in folder_details['links'].iteritems()]

            if 'extra' not in args['info']['title'] and 'extra' not in args['showInfo']['info']['tvshowtitle'] \
                    and int(args['info']['season']) != 0:
                folder_details = [i for i in folder_details if
                                  'extra' not in
                                  source_utils.cleanTitle(i['filename'].replace('&', ' ').lower())]

            if 'special' not in args['info']['title'] and 'special' not in args['showInfo']['info']['tvshowtitle'] \
                    and int(args['info']['season']) != 0:
                folder_details = [i for i in folder_details if
                                  'special' not in
                                  source_utils.cleanTitle(i['filename'].replace('&', ' ').lower())]

            streamLink = self.check_episode_string(folder_details, episodeStrings)

            if streamLink is None:
                return

            return self.resolve_hoster(streamLink)
        except:
            import traceback
            traceback.print_exc()
            pass

    def check_episode_string(self, folder_details, episodeStrings):
        for i in folder_details:
            for epstring in episodeStrings:
                if epstring in source_utils.cleanTitle(i['filename'].replace('&', ' ').lower()):
                    if any(i['filename'].endswith(ext) for ext in source_utils.COMMON_VIDEO_EXTENSIONS):
                        return i['link']
        return None
