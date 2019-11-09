# -*- coding: utf-8 -*-

import json
import threading
from time import sleep

import requests

from resources.lib.modules import control


class TraktAPI:
    def __init__(self):

        self.ApiUrl = 'https://api.trakt.tv/'
        self.BaseUrl = 'https://trakt.tv'

        self.ClientID = ''
        self.ClientID = control.getSetting('trakt.clientid')
        if self.ClientID == '':
            self.ClientID = '7a34adf6d9b2ec3f6275dcb637249dbeb7a07df6fa8807ab6622a3899f62c712'

        self.ClientSecret = ''
        self.ClientSecret = control.getSetting('trakt.secret')
        if self.ClientSecret == '':
            self.ClientSecret = '8c9507da0f59e835dcd575bee327c0e80437caf9459d2288ac09e5d5da00a5fb'

        self.RedirectUri = 'urn:ietf:wg:oauth:2.0:oob'
        self.AccessToken = control.getSetting('trakt.auth')
        self.RefreshToken = control.getSetting('trakt.refresh')

        self.headers = {'trakt-api-version': '2',
                        'trakt-api-key': self.ClientID,
                        'content-type': 'application/json'}

        if not self.AccessToken is '':
            self.headers['Authorization'] = 'Bearer %s' % self.AccessToken

        self.response_headers = {}
        self.response_code = 0

    def revokeAuth(self):
        url = "oauth/revoke"
        postData = {"token": control.getSetting('trakt.auth')}
        self.post_request(url, postData, limit=False)
        control.setSetting('trakt.auth', '')
        control.setSetting('trakt.refresh', '')
        control.setSetting('trakt.username', '')
        from resources.lib.modules.trakt_sync import activities
        database = activities.TraktSyncDatabase()
        database.clear_user_information()
        control.showDialog.ok(control.addonName, control.lang(32030))

    def auth(self):

        url = 'https://api.trakt.tv/oauth/device/code'
        postData = {'client_id': self.ClientID}
        response = requests.post(url, data=postData)
        if not response.ok:
            control.showDialog.ok(control.addonName, control.lang(40113))
            return
        response = json.loads(response.text)
        try:
            user_code = response['user_code']
            device = response['device_code']
            interval = int(response['interval'])
            expiry = int(response['expires_in'])
        except:
            control.showDialog.ok(control.addonName, control.lang(32032))
            return
        currentTime = 0
        control.copy2clip(user_code)
        control.progressDialog.create(control.addonName + ': ' + control.lang(32031),
                                    control.lang(32024) +
                                    control.colorString('https://trakt.tv/activate \n') +
                                    control.lang(32025) + control.colorString(user_code) + "\n" +
                                    control.lang(32071)

                                    )
        control.progressDialog.update(100)
        while currentTime < (expiry - interval):
            if control.progressDialog.iscanceled():
                control.progressDialog.close()
                return
            progressPercent = int(100 - ((float(currentTime) / expiry) * 100))
            control.progressDialog.update(progressPercent)
            sleep(interval)
            postData = {'code': device, 'client_id': self.ClientID, 'client_secret': self.ClientSecret}
            url = 'https://api.trakt.tv/oauth/device/token'
            response = requests.post(url, data=postData)

            if '200' in str(response):
                response = json.loads(response.text)
                control.setSetting('trakt.auth', response['access_token'])
                control.setSetting('trakt.refresh', response['refresh_token'])
                self.AccessToken = response['access_token']
                self.headers = {'trakt-api-version': '2',
                                'trakt-api-key': self.ClientID,
                                'content-type': 'application/json'}

                if not self.AccessToken is '':
                    self.headers['Authorization'] = 'Bearer %s' % self.AccessToken
                username = self.get_username()
                control.setSetting('trakt.username', username)
                control.progressDialog.close()
                control.showDialog.ok(control.addonName, control.lang(40263))

                # Synchronise Trakt Database with new user
                from resources.lib.modules.trakt_sync import activities
                database = activities.TraktSyncDatabase()
                if database.activites['trakt_username'] != username:
                    database.clear_user_information()
                    database.flush_activities(False)
                    database._build_sync_activities()
                    database.set_trakt_user(username)
                    control.execute('RunPlugin("plugin://plugin.video.%s/?action=syncTraktActivities")' %
                                  control.addonName.lower())
                break
            if '400' in str(response):
                pass
            else:
                control.progressDialog.close()
                control.showDialog.ok(control.addonName, control.lang(32032))
                break

    def refreshToken(self):
        url = self.ApiUrl + "/oauth/token"
        postData = {
            'refresh_token': self.RefreshToken,
            'client_id': self.ClientID,
            'client_secret': self.ClientSecret,
            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
            'grant_type': 'refresh_token'
        }
        response = requests.post(url, data=postData)
        try:
            response = json.loads(response.text)
            control.setSetting('trakt.auth', response['access_token'])
            control.setSetting('trakt.refresh', response['refresh_token'])
            self.AccessToken = response['access_token']
            self.RefreshToken = response['refresh_token']
            control.log('Refreshed Trakt Token')
            if not self.AccessToken is '':
                self.headers['Authorization'] = self.AccessToken
            return
        except:
            import traceback
            traceback.print_exc()
            control.log('Failed to refresh Trakt Access Token', 'error')
            return

    def get_request(self, url, limit=True, limitOverride=0, refreshCheck=False):

        if refreshCheck == False:
            url = self.ApiUrl + url
            if limit == True:
                if limitOverride == 0:
                    limitAmount = int(control.getSetting('item.limit'))
                else:
                    limitAmount = limitOverride
                if not '?' in url:
                    url += '?limit=%s' % limitAmount
                else:
                    url += '&limit=%s' % limitAmount

        try:
            response = requests.get(url, headers=self.headers)
            self.response_headers = response.headers
            if response.status_code == 401:
                control.log('Trakt OAuth Failure, %s %s' % (str(response.text), response.request.headers), 'info')
                if refreshCheck == False:
                    self.refreshToken()
                    self.get_request(url, refreshCheck=True)
                else:
                    control.log('Failed to perform request even after token refresh', 'error')
            if response.status_code > 499:
                control.log('Trakt is having issues with their servers', 'error')
                return None
            if response.status_code == 404:
                control.log('Trakt returned a 404', 'error')
                return None
            if response.status_code == 502:
                control.log('Trakt is currently experiencing Gateway Issues', 'error')
        except requests.exceptions.ConnectionError:
            return
        except not requests.exceptions.ConnectionError:
            control.showDialog.ok(control.addonName, control.lang(32035))
            return

        return response.text

    def post_request(self, url, postData, limit=True, refreshCheck=False):
        if refreshCheck == False:
            url = self.ApiUrl + url
            if limit == True:
                limitAmount = control.getSetting('item.limit')
                if not '?' in url:
                    url += '?limit=%s' % limitAmount
                else:
                    url += '&limit=%s' % limitAmount
        try:
            response = requests.post(url, json=postData, headers=self.headers)
            self.response_headers = response.headers
            if response.status_code == 401:
                if refreshCheck == False:
                    self.refreshToken()
                    self.post_request(url, postData, limit=limit, refreshCheck=True)
                else:
                    control.log('Failed to perform trakt request even after token refresh', 'error')

            if response.status_code > 499:
                return None

        except requests.exceptions.ConnectionError:
            return
        except not requests.exceptions.ConnectionError:
            control.showDialog.ok(control.addonName, control.lang(32035))
            return

        return response.text

    def delete_request(self, url, refreshCheck=False):
        if refreshCheck == False:
            url = self.ApiUrl + url

        try:
            response = requests.delete(url, headers=self.headers)
            if response.status_code == 401:
                if refreshCheck == False:
                    self.refreshToken()
                    self.delete_request(url, refreshCheck=True)
                else:
                    control.log('Failed to perform trakt request even after token refresh', 'error')

            if response.status_code > 499:
                return None

        except requests.exceptions.ConnectionError:
            return
        except not requests.exceptions.ConnectionError:
            control.showDialog.ok(control.addonName, control.lang(32035))
            return

        return response.text

    def json_response(self, url, postData=None, limit=True, limitOverride=0):
        if postData is None:
            response = self.get_request(url, limit=limit, limitOverride=limitOverride)
        else:
            response = self.post_request(url, postData, limit=limit)
        try:
            response = json.loads(response)
        except:
            return None
        return response

    @staticmethod
    def _get_display_name(type):
        if type == 'movie':
            return control.lang(40279)
        else:
            return control.lang(40276)

    def traktManager(self, actionArgs):

        trakt_object = control.get_item_information(actionArgs)['trakt_object']

        actionArgs = json.loads(control.unquote(actionArgs))

        type = actionArgs['item_type'].lower()

        display_type = self._get_display_name(type)

        trakt_object['show_id'] = actionArgs['trakt_id']
        
        if trakt_object is None:
            control.showDialog.notification(control.addonName, control.lang(40264))

        dialog_list = [control.lang(40265), control.lang(40266), control.lang(40267), control.lang(40268), control.lang(40269),
                       control.lang(40270), control.lang(40271), control.lang(40272), control.lang(40273) % display_type,
                       control.lang(40274), control.lang(40275)]

        if type in ['show', 'season']:
            dialog_list.pop(10)

        selection = control.showDialog.select('{}: {}'.format(control.addonName, control.lang(40280)), dialog_list)
        thread = None

        if selection == 0:
            thread = threading.Thread(target=self.addToCollection, args=(trakt_object,))
        elif selection == 1:
            thread = threading.Thread(target=self.removeFromCollection, args=(trakt_object,))
        elif selection == 2:
            thread = threading.Thread(target=self.addToWatchList, args=(trakt_object,))
        elif selection == 3:
            thread = threading.Thread(target=self.removeFromWatchlist, args=(trakt_object,))
        elif selection == 4:
            thread = threading.Thread(target=self.markWatched, args=(trakt_object, actionArgs))
        elif selection == 5:
            thread = threading.Thread(target=self.markUnwatched, args=(trakt_object, actionArgs))
        elif selection == 6:
            self.addToList(trakt_object)
        elif selection == 7:
            self.removeFromList(trakt_object)
        elif selection == 8:
            self.hideItem(actionArgs)
        elif selection == 9:
            self.refresh_meta_information(trakt_object)
        elif selection == 10:
            self.removePlaybackHistory(trakt_object)
        else:
            return

        if thread is not None:
            thread.start()

        return

    def refresh_meta_information(self, trakt_object):
        from resources.lib.modules import trakt_sync
        trakt_sync.TraktSyncDatabase().clear_specific_meta(trakt_object)
        control.execute('Container.Refresh')

    def confirm_marked_watched(self, response, type):
        try:

            if response['added'][type] > 0:
                return True

            raise Exception

        except Exception as e:
            control.showDialog.notification('{}: {}'.format(control.addonName, control.lang(40280)), control.lang(40281))
            control.log('Failed to mark item as watched, error: %s \n Trakt Response: %s' % (e, response))

            return False

    def confirm_marked_unwatched(self, response, type):
        try:
            if response['deleted'][type] > 0:
                return True

            raise Exception

        except Exception as e:
            control.showDialog.notification('{}: {}'.format(control.addonName, control.lang(40280)), control.lang(40281))
            control.log('Failed to mark item as unwatched, error: %s \n Trakt Response: %s' % (e, response))

            return False

    def markWatched(self, trakt_object, actionArgs):
        response = self.json_response('sync/history', postData=trakt_object)

        if 'episodes' in trakt_object:
            if not self.confirm_marked_watched(response, 'episodes'):
                return
            from resources.lib.modules.trakt_sync.shows import TraktSyncDatabase
            trakt_object = trakt_object['episodes'][0]
            TraktSyncDatabase().mark_episode_watched_by_id(trakt_object['ids']['trakt'])

        elif 'seasons' in trakt_object:
            if not self.confirm_marked_watched(response, 'episodes'):
                return
            from resources.lib.modules.trakt_sync.shows import TraktSyncDatabase
            show_id = actionArgs['trakt_id']
            season_no = trakt_object['seasons'][0]['number']
            TraktSyncDatabase().mark_season_watched(show_id, season_no, 1)

        elif 'shows' in trakt_object:
            if not self.confirm_marked_watched(response, 'episodes'):
                return
            from resources.lib.modules.trakt_sync.shows import TraktSyncDatabase
            trakt_object = trakt_object['shows'][0]
            TraktSyncDatabase().mark_show_watched(trakt_object['ids']['trakt'], 1)

        elif 'movies' in trakt_object:
            if not self.confirm_marked_watched(response, 'movies'):
                return
            from resources.lib.modules.trakt_sync.movies import TraktSyncDatabase
            trakt_object = trakt_object['movies'][0]
            TraktSyncDatabase().mark_movie_watched(trakt_object['ids']['trakt'])

        control.showDialog.notification('{}: {}'.format(control.addonName, control.lang(40280)), control.lang(40281))
        control.trigger_widget_refresh()

    def markUnwatched(self, trakt_object, actionArgs):

        response = self.json_response('sync/history/remove', postData=trakt_object)

        if 'episodes' in trakt_object:
            if not self.confirm_marked_unwatched(response, 'episodes'):
                return
            from resources.lib.modules.trakt_sync.shows import TraktSyncDatabase
            trakt_object = trakt_object['episodes'][0]
            TraktSyncDatabase().mark_episode_unwatched_by_id(trakt_object['ids']['trakt'])

        elif 'seasons' in trakt_object:

            from resources.lib.modules.trakt_sync.shows import TraktSyncDatabase
            if not self.confirm_marked_unwatched(response, 'episodes'):
                return
            show_id = actionArgs['trakt_id']
            season_no = trakt_object['seasons'][0]['number']
            TraktSyncDatabase().mark_season_watched(show_id, season_no, 0)

        elif 'shows' in trakt_object:
            from resources.lib.modules.trakt_sync.shows import TraktSyncDatabase
            if not self.confirm_marked_unwatched(response, 'episodes'):
                return
            trakt_object = trakt_object['shows'][0]
            TraktSyncDatabase().mark_show_watched(trakt_object['ids']['trakt'], 0)

        elif 'movies' in trakt_object:
            from resources.lib.modules.trakt_sync.movies import TraktSyncDatabase
            if not self.confirm_marked_unwatched(response, 'movies'):
                return
            trakt_object = trakt_object['movies'][0]
            TraktSyncDatabase().mark_movie_unwatched(trakt_object['ids']['trakt'])

        control.showDialog.notification('{}: {}'.format(control.addonName, control.lang(40280)), control.lang(40283))
        control.trigger_widget_refresh()

    def addToCollection(self, trakt_object):

        self.post_request('sync/collection', postData=trakt_object)

        if 'seasons' in trakt_object:
            from resources.lib.modules.trakt_sync.shows import TraktSyncDatabase
            trakt_object = trakt_object['seasons'][0]
            TraktSyncDatabase().mark_season_collected(trakt_object['ids']['trakt'], trakt_object['number'], 1)
        if 'shows' in trakt_object:
            from resources.lib.modules.trakt_sync.shows import TraktSyncDatabase
            trakt_object = trakt_object['shows'][0]
            TraktSyncDatabase().mark_show_collected(trakt_object['ids']['trakt'], 1)
        if 'episodes' in trakt_object:
            from resources.lib.modules.trakt_sync.shows import TraktSyncDatabase
            trakt_object = trakt_object['episodes'][0]
            TraktSyncDatabase().mark_episode_collected(trakt_object['ids']['trakt'], trakt_object['season'],
                                                       trakt_object['number'])
        if 'movies' in trakt_object:
            from resources.lib.modules.trakt_sync.movies import TraktSyncDatabase
            trakt_object = trakt_object['movies'][0]
            TraktSyncDatabase().mark_movie_collected(trakt_object['ids']['trakt'])

        control.showDialog.notification('{}: {}'.format(control.addonName, control.lang(40280)), control.lang(40284))

    def removeFromCollection(self, trakt_object):
        self.post_request('sync/collection/remove', postData=trakt_object)

        if 'seasons' in trakt_object:
            from resources.lib.modules.trakt_sync.shows import TraktSyncDatabase
            trakt_object = trakt_object['seasons'][0]
            TraktSyncDatabase().mark_season_collected(trakt_object['ids']['trakt'], trakt_object['number'], 0)
        if 'shows' in trakt_object:
            from resources.lib.modules.trakt_sync.shows import TraktSyncDatabase
            trakt_object = trakt_object['shows'][0]
            TraktSyncDatabase().mark_show_collected(trakt_object['ids']['trakt'], 0)
        if 'episodes' in trakt_object:
            from resources.lib.modules.trakt_sync.shows import TraktSyncDatabase
            trakt_object = trakt_object['episodes'][0]
            TraktSyncDatabase().mark_episode_uncollected(trakt_object['ids']['trakt'], trakt_object['season'],
                                                         trakt_object['number'])
        if 'movies' in trakt_object:
            from resources.lib.modules.trakt_sync.movies import TraktSyncDatabase
            trakt_object = trakt_object['movies'][0]
            TraktSyncDatabase().mark_movie_uncollected(trakt_object['ids']['trakt'])

        control.showDialog.notification('{}: {}'.format(control.addonName, control.lang(40280)), control.lang(40285))

    def addToWatchList(self, trakt_object):
        self.post_request('sync/watchlist', postData=trakt_object)
        control.showDialog.notification('{}: {}'.format(control.addonName, control.lang(40280)), control.lang(40286))

    def removeFromWatchlist(self, trakt_object):
        self.post_request('sync/watchlist/remove', postData=trakt_object)
        control.showDialog.notification('{}: {}'.format(control.addonName, control.lang(40280)), control.lang(40287))

    def addToList(self, trakt_object):
        lists = self.getLists()
        selection = control.showDialog.select('{}: {}'.format(control.addonName, control.lang(40290)),
                                            [i['name'] for i in lists])
        selection = lists[selection]
        self.json_response('users/me/lists/%s/items' % selection['ids']['trakt'], postData=trakt_object)
        control.showDialog.notification('{}: {}'.format(control.addonName, control.lang(40280)),
                                      control.lang(40288) % selection['name'])

    def removeFromList(self, trakt_object):
        lists = self.getLists()
        selection = control.showDialog.select('{}: {}'.format(control.addonName, control.lang(40290)),
                                            [i['name'] for i in lists])
        selection = lists[selection]
        self.json_response('users/me/lists/%s/items/remove' % selection['ids']['trakt'], postData=trakt_object)
        control.showDialog.notification('{}: {}'.format(control.addonName, control.lang(40280)),
                                      control.lang(40289) % selection['name'])

    def hideItem(self, trakt_object):
        from resources.lib.modules.trakt_sync.hidden import TraktSyncDatabase

        sections = ['progress_watched', 'calendar']
        sections_display = [control.lang(40291), control.lang(40292)]
        selection = control.showDialog.select('{}: {}'.format(control.addonName, control.lang(40293)), sections_display)
        section = sections[selection]

        if trakt_object['item_type'] in ['season', 'show', 'episode']:
            trakt_object = {'shows': [{'ids': {'trakt': trakt_object['trakt_id']}}]}
        elif trakt_object['item_type'] == 'movie':
            trakt_object = {'movies': [{'ids': {'trakt': trakt_object['trakt_id']}}]}

        self.json_response('users/hidden/%s' % section, postData=trakt_object)

        if 'movies' in trakt_object:
            trakt_object = trakt_object['movies'][0]
            TraktSyncDatabase().add_hidden_item(trakt_object['ids']['trakt'], 'movie', section)
        if 'shows' in trakt_object:
            trakt_object = trakt_object['shows'][0]
            TraktSyncDatabase().add_hidden_item(trakt_object['ids']['trakt'], 'show', section)

        control.showDialog.notification(control.addonName, control.lang(40294) % sections_display[selection])

    def removePlaybackHistory(self, trakt_object):
        type = 'movie'
        multi_type = 'movies'

        if 'episodes' in trakt_object:
            type = 'episode'
            multi_type = 'episodes'

        progress = self.json_response('sync/playback/%s' % multi_type, limit=False)
        progress = [i for i in progress if i['type'] == type]
        progress = [i for i in progress
                    if i[type]['ids']['trakt'] == trakt_object[multi_type][0]['ids']['trakt']]

        for i in progress:
            self.delete_request('sync/playback/%s' % i['id'])

        control.showDialog.notification(control.addonName, control.lang(40295))

    def get_username(self):
        user_details = json.loads(self.get_request('users/me'))
        return user_details['username']

    def getLists(self, username='me'):
        lists = self.json_response('users/%s/lists' % username, limit=True, limitOverride=500)
        return lists

    def myTraktLists(self, media_type):

        lists = self.getLists()

        try:
            liked_lists = [i for i in self.json_response('users/likes/lists', limit=True, limitOverride=500)]
            liked_lists = [i['list'] for i in liked_lists]
            lists += liked_lists

        except:

            import traceback
            traceback.print_exc()
            pass

        for user_list in lists:
            arguments = {'trakt_id': user_list['ids']['slug'],
                         'username': user_list['user']['ids']['slug'],
                         'type': media_type,
                         'sort_how': user_list['sort_how'],
                         'sort_by': user_list['sort_by']
                         }

            control.addDirectoryItem(user_list['name'],
                                   'traktList&page=1&actionArgs=%s' % control.quote(json.dumps(arguments)))

        control.closeDirectory('addons')
        return

    def sort_list(self, sort_by, sort_how, list_items, media_type):
        supported_sorts = ['added', 'rank', 'title', 'released', 'runtime', 'popularity', 'votes', 'random']

        if sort_by == 'added':
            list_items = sorted(list_items, key=lambda x: x['listed_at'])
        if sort_by == 'rank':
            list_items = sorted(list_items, key=lambda x: x['rank'])
        if sort_by == 'title':
            list_items = sorted(list_items, key=lambda x: x[media_type]['title'].lower().replace('the ', ''))
        if sort_by == 'released':
            try:
                list_items = sorted(list_items, key=lambda x: x[media_type]['released'])
            except:
                list_items = sorted(list_items, key=lambda x: x[media_type]['first_aired'])
        if sort_by == 'runtime':
            if 'aired_episodes' in list_items[0][media_type]:
                list_items = sorted(list_items, key=lambda x:
                (x[media_type]['runtime'] * x[media_type]['aired_episodes']))
            else:
                list_items = sorted(list_items, key=lambda x: x[media_type]['runtime'])
        if sort_by == 'popularity':
            list_items = sorted(list_items, key=lambda x: x[media_type]['rating'])
        if sort_by == 'votes':
            list_items = sorted(list_items, key=lambda x: x[media_type]['votes'])
        if sort_by == 'random':
            import random
            list_items = random.shuffle(list_items)

        if sort_by not in supported_sorts:
            return list_items

        if sort_how == 'desc':
            list_items.reverse()

        return list_items

    def getListItems(self, arguments, page):

        arguments = json.loads(control.unquote(arguments))
        media_type = arguments['type']
        username = control.quote_plus(arguments['username'])
        url = 'users/%s/lists/%s/items/%s?extended=full' % (username, arguments['trakt_id'], media_type)
        list_items = self.json_response(url, None, False)

        if list_items is None or len(list_items) == 0:
            return

        if media_type == 'movies':
            media_type = 'movie'

        if media_type == 'shows':
            media_type = 'show'

        list_items = self.sort_list(arguments['sort_by'], arguments['sort_how'], list_items, media_type)

        if media_type == 'show':
            list_items = [i['show'] for i in list_items if i['type'] == 'show' and i is not None]
            from resources.lib.indexers import tvshowMenus
            tvshowMenus.Menus().showListBuilder(list_items)

        if media_type == 'movie':
            list_items = [i['movie'] for i in list_items if i['type'] == 'movie' and i is not None]
            from resources.lib.indexers import movieMenus
            movieMenus.Menus().commonListBuilder(list_items)

        content_type = 'tvshows'

        if media_type == 'movie':
            content_type = 'movies'

        control.closeDirectory(content_type)
        return
