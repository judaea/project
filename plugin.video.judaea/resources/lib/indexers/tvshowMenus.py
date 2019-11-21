# -*- coding: utf-8 -*-

import datetime
import json
import sys
from resources.lib.modules import control
from resources.lib.modules.worker import ThreadPool
from resources.lib.modules.trakt import TraktAPI
from resources.lib.modules import database
from resources.lib.modules.trakt_sync.hidden import TraktSyncDatabase as HiddenDatabase
from resources.lib.modules.trakt_sync.shows import TraktSyncDatabase

sysaddon = sys.argv[0]
try:
    syshandle = int(sys.argv[1])
except:
    syshandle = ''
trakt = TraktAPI()

language_code = control.get_language_code()

trakt_database = TraktSyncDatabase()
hidden_database = HiddenDatabase()


class Menus:
    def __init__(self):
        self.itemList = []
        self.direct_episode_threads = []
        self.title_appends = control.getSetting('general.appendtitles')
        self.task_queue = ThreadPool()

    ######################################################
    # MENUS
    ######################################################

    def onDeckShows(self):
        hidden_shows = hidden_database.get_hidden_items('progress_watched', 'shows')
        trakt_list = trakt.json_response('sync/playback/episodes', limit=True)

        if trakt_list is None:
            return
        trakt_list = [i for i in trakt_list if i['show']['ids']['trakt'] not in hidden_shows]
        trakt_list = sorted(trakt_list, key=lambda i: control.datetime_workaround(i['paused_at'][:19],
                                                                                format="%Y-%m-%dT%H:%M:%S",
                                                                                date_only=False), reverse=True)
        filter_list = []
        showList = []
        sort_list = []
        for i in trakt_list:
            if i['show']['ids']['trakt'] not in filter_list:
                if int(i['progress']) != 0:
                    showList.append(i)
                    filter_list.append(i['show']['ids']['trakt'])
                    sort_list.append(i['show']['ids']['trakt'])

        sort = {'type': 'showInfo', 'id_list': sort_list}
        self.mixedEpisodeBuilder(showList, sort=sort)
        control.closeDirectory('tvshows')

    def discoverShows(self):

        control.addDirectoryItem(control.lang(32007), 'showsPopular&page=1')
        control.addDirectoryItem(control.lang(32009), 'showsTrending&page=1')
        control.addDirectoryItem(control.lang(32067), 'showsNew')
        control.addDirectoryItem(control.lang(32010), 'showsPlayed&page=1')
        control.addDirectoryItem(control.lang(32011), 'showsWatched&page=1')
        control.addDirectoryItem(control.lang(32012), 'showsCollected&page=1')
        control.addDirectoryItem(control.lang(32013), 'showsAnticipated&page=1')
        control.addDirectoryItem(control.lang(32014), 'showsUpdated&page=1')
        if control.getSetting('trakt.auth') is not '':
            control.addDirectoryItem(control.lang(32008), 'showsRecommended')
        control.addDirectoryItem(control.lang(40121), 'showsNetworks')
        control.addDirectoryItem(control.lang(40123), 'showYears')
        control.addDirectoryItem(control.lang(32062), 'tvGenres')
        control.addDirectoryItem(control.lang(40151), 'showsByActor')
        # show genres is now labeled as tvGenres to support genre icons in skins
        if control.getSetting('searchHistory') == 'false':
            control.addDirectoryItem(control.lang(32016), 'showsSearch', isFolder=True, isPlayable=False)
        else:
            control.addDirectoryItem(control.lang(32016), 'showsSearchHistory')
        control.closeDirectory('addons')

    def myShows(self):
        control.addDirectoryItem(control.lang(40172), 'showsNextUp')
        control.addDirectoryItem(control.lang(32017), 'showsMyCollection')
        control.addDirectoryItem(control.lang(32018), 'showsMyWatchlist')
        control.addDirectoryItem(control.lang(40173), 'myUpcomingEpisodes')
        control.addDirectoryItem(control.lang(40174), 'showsMyProgress')
        control.addDirectoryItem(control.lang(40175), 'showsMyRecentEpisodes')
        control.addDirectoryItem(control.lang(32008), 'showsRecommended')
        control.addDirectoryItem(control.lang(32063), 'onDeckShows')
        control.addDirectoryItem(control.lang(40176), 'myTraktLists&actionArgs=shows')
        control.closeDirectory('addons')

    def myShowCollection(self):
        trakt_list = trakt_database.get_collected_episodes()
        trakt_list = [i for i in trakt_list if i is not None]
        trakt_list = list(set([i['show_id'] for i in trakt_list]))
        trakt_list = [{'ids': {'trakt': i}} for i in trakt_list]
        trakt_list = [i for i in trakt_list if i is not None]
        if trakt_list is None:
            return
        self.showListBuilder(trakt_list)
        control.closeDirectory('tvshows', sort='title')

    def myShowWatchlist(self):
        trakt_list = trakt.json_response('users/me/watchlist/shows', limit=False)
        if trakt_list is None:
            return
        try:
            sort_by = trakt.response_headers['X-Sort-By']
            sort_how = trakt.response_headers['X-Sort-How']
            trakt_list = trakt.sort_list(sort_by, sort_how, trakt_list, 'show')
        except:
            control.log('Failed to sort trakt list by response headers', 'error')
            pass
        self.showListBuilder(trakt_list)
        control.closeDirectory('tvshows')

    def myProgress(self):

        collected_episodes = trakt_database.get_collected_episodes()
        collection = list(set([i['show_id'] for i in collected_episodes]))
        if len(collection) == 0:
            return

        show_dicts = []
        for i in collection:
            show_dicts.append({'show': {'ids': {'trakt': i}}})

        show_meta_list = trakt_database.get_show_list(show_dicts)
        unfinished = []

        for show in show_meta_list:
            if show['info']['playcount'] == 0:
                unfinished.append(show)

        self.showListBuilder(unfinished)
        control.closeDirectory('tvshows', sort='title')

    def newShows(self):

        hidden = hidden_database.get_hidden_items('recommendations', 'shows')
        datestring = datetime.datetime.today() - datetime.timedelta(days=29)
        trakt_list = database.get(trakt.json_response, 12, 'calendars/all/shows/new/%s/30?languages=%s' %
                                  (datestring.strftime('%d-%m-%Y'), language_code))

        if trakt_list is None:
            return
        # For some reason trakt messes up their list and spits out tons of duplicates so we filter it
        duplicate_filter = []
        temp_list = []
        for i in trakt_list:
            if not i['show']['ids']['tvdb'] in duplicate_filter:
                duplicate_filter.append(i['show']['ids']['tvdb'])
                temp_list.append(i)

        trakt_list = temp_list

        trakt_list = [i for i in trakt_list if i['show']['ids']['trakt'] not in hidden]

        if len(trakt_list) > 40:
            trakt_list = trakt_list[:40]
        self.showListBuilder(trakt_list)
        control.closeDirectory('tvshows')

    def myNextUp(self, ):

        watched_shows = trakt_database.get_watched_shows()
        hidden_shows = hidden_database.get_hidden_items('progress_watched', 'shows')

        watched_shows = [i for i in watched_shows if i['trakt_id'] not in hidden_shows]
        watched_episodes = trakt_database.get_watched_episodes()

        for show in watched_shows:
            self.task_queue.put(self._get_next_episode_to_watch, show, watched_episodes)

        self.task_queue.wait_completion()

        if control.getSetting('nextup.sort') == '1':
            watched_list = trakt.json_response('users/me/watched/shows')
            watched_list = sorted(watched_list, key=lambda i: i['last_watched_at'], reverse=True)
            watched_list = [i['show']['ids']['trakt'] for i in watched_list]
            sort = {'type': 'showInfo', 'id_list': watched_list}
        else:
            sort = None

        episodes = self.itemList
        self.itemList = []

        self.mixedEpisodeBuilder(episodes, sort=sort, hide_watched=True)

        control.closeDirectory('tvshows')

    def _get_next_episode_to_watch(self, show_db_dict, watched_episodes):
        try:
            show_id = show_db_dict['trakt_id']

            if show_db_dict['kodi_meta'] == {}:
                show_db_dict['kodi_meta'] = trakt_database.get_single_show(show_id)

            watched_episodes = [i for i in watched_episodes if i['show_id'] == show_id]
            watched_episodes = sorted(watched_episodes, key=lambda episode: episode['season'], reverse=True)

            season = watched_episodes[0]['season']
            season_meta = trakt_database.get_single_season(show_id, season)

            watched_episodes = [i for i in watched_episodes if i['season'] == season]
            watched_episodes = sorted(watched_episodes, key=lambda episode: episode['number'], reverse=True)
            last_watched_episode = watched_episodes[0]['number']
            next_episode = int(watched_episodes[0]['number']) + 1

            if season_meta is None:
                control.log('Could not acquire season meta information for %s Season %s' % (show_id, season), 'error')
                return

            if season_meta['info']['episode_count'] == len(watched_episodes) \
                    or season_meta['info']['episode_count'] == last_watched_episode:

                if int(show_db_dict['kodi_meta']['info']['season_count']) > season:
                    season += 1
                    next_episode = 1

            episode_dict = {'show': {'ids': {'trakt': show_id}},
                            'episode': {'season': season, 'number': next_episode}}

            self.itemList.append(episode_dict)
        except KeyError:
            import traceback
            traceback.print_exc()
            pass
        except:
            import traceback
            traceback.print_exc()

    def myRecentEpisodes(self):
        hidden_shows = hidden_database.get_hidden_items('calendar', 'shows')
        datestring = datetime.datetime.today() - datetime.timedelta(days=13)
        trakt_list = database.get(trakt.json_response, 12, 'calendars/my/shows/%s/14' %
                                  datestring.strftime('%d-%m-%Y'))

        if trakt_list is None:
            return
        trakt_list = [i for i in trakt_list if i['show']['ids']['trakt'] not in hidden_shows]
        self.mixedEpisodeBuilder(trakt_list)
        control.closeDirectory('episodes')

    def myUpcomingEpisodes(self):
        tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        upcoming_episodes = database.get(trakt.json_response, 24, 'calendars/my/shows/%s/30' % tomorrow)

        sort = sorted(upcoming_episodes, key=lambda i: i['first_aired'])
        sort = [i['episode']['ids']['trakt'] for i in sort]
        sort = {'type': None, 'id_list': sort}
        self.mixedEpisodeBuilder(upcoming_episodes, sort=sort, hide_watched=False, hide_unaired=False,
                                 prepend_date=True)
        control.closeDirectory('episodes')

    def showsNetworks(self):
        trakt_list = database.get(trakt.json_response, 24, 'networks')

        if trakt_list is None:
            return
        list_items = []
        for i in trakt_list:
            list_items.append(control.addDirectoryItem(i['name'], 'showsNetworkShows&actionArgs=%s&page=1' % i['name'],
                                                     '', '', bulk_add=True))
        control.addMenuItems(syshandle, list_items, len(list_items))
        control.closeDirectory('addons')

    def showsNetworkShows(self, network, page):

        trakt_list = database.get(trakt.json_response, 24, 'shows/popular?networks=%s&page=%s' % (network, page))

        if trakt_list is None:
            return

        self.showListBuilder(trakt_list)

        if len(trakt_list) == int(control.getSetting('item.limit')):
            control.addDirectoryItem(control.lang(32019), 'showsNetworkShows&actionArgs=%s&page=%s' %
                                   (network, int(page) + 1))

        control.closeDirectory('tvshows')

    def showsPopular(self, page):
        trakt_list = database.get(trakt.json_response, 12, 'shows/popular?page=%s' % page)

        if trakt_list is None:
            return

        self.showListBuilder(trakt_list)
        control.addDirectoryItem(control.lang(32019), 'showsPopular&page=%s' % (int(page) + 1))
        control.closeDirectory('tvshows')

    def showsRecommended(self):
        trakt_list = database.get(trakt.json_response, 12, 'recommendations/shows?ignore_collected=true',
                                  limit=True, limitOverride=100)
        if trakt_list is None:
            return
        self.showListBuilder(trakt_list)
        control.closeDirectory('tvshows')

    def showsTrending(self, page):
        trakt_list = database.get(trakt.json_response, 12, 'shows/trending?page=%s' % page)
        if trakt_list is None:
            return
        self.showListBuilder(trakt_list)
        control.addDirectoryItem(control.lang(32019), 'showsTrending&page=%s' % (int(page) + 1))
        control.closeDirectory('tvshows')

    def showsPlayed(self, page):
        trakt_list = database.get(trakt.json_response, 12, 'shows/played?page=%s' % page)
        if trakt_list is None:
            return
        self.showListBuilder(trakt_list)
        control.addDirectoryItem(control.lang(32019), 'showsPlayed&page=%s' % (int(page) + 1))
        control.closeDirectory('tvshows')

    def showsWatched(self, page):
        trakt_list = database.get(trakt.json_response, 12, 'shows/watched?page=%s' % page)
        if trakt_list is None:
            return
        self.showListBuilder(trakt_list)
        control.addDirectoryItem(control.lang(32019), 'showsWatched&page=%s' % (int(page) + 1))
        control.closeDirectory('tvshows')

    def showsCollected(self, page):
        trakt_list = database.get(trakt.json_response, 12, 'shows/collected?page=%s' % page)
        if trakt_list is None:
            return
        self.showListBuilder(trakt_list)
        control.addDirectoryItem(control.lang(32019), 'showsCollected&page=%s' % (int(page) + 1))
        control.closeDirectory('tvshows')

    def showsAnticipated(self, page):
        trakt_list = database.get(trakt.json_response, 12, 'shows/anticipated?page=%s&language=%s'
                                  % (page, language_code))
        if trakt_list is None:
            return
        self.showListBuilder(trakt_list)
        control.addDirectoryItem(control.lang(32019), 'showsAnticipated&page=%s' % (int(page) + 1))
        control.closeDirectory('tvshows')

    def showsUpdated(self, page):
        import datetime
        date = datetime.date.today() - datetime.timedelta(days=31)
        date = date.strftime('%Y-%m-%d')
        trakt_list = database.get(trakt.json_response, 12, 'shows/updates/%s?page=%s' % (date, page))
        if trakt_list is None:
            return
        self.showListBuilder(trakt_list)
        control.addDirectoryItem(control.lang(32019), 'showsUpdated&page=%s' % (int(page) + 1))
        control.closeDirectory('tvshows')

    def showSearchHistory(self):
        history = database.getSearchHistory('show')
        control.addDirectoryItem(control.lang(40142), 'showsSearch', isFolder=True, isPlayable=False)
        control.addDirectoryItem(control.lang(40140), 'clearSearchHistory', isFolder=False, isPlayable=False)

        for i in history:
            control.addDirectoryItem(i, 'showsSearchResults&actionArgs=%s' % control.quote(i))
        control.closeDirectory('addon')

    def showsSearch(self, actionArgs=None):

        if actionArgs == None:
            k = control.showKeyboard('', control.lang(32016))
            k.doModal()
            query = (k.getText() if k.isConfirmed() else None)
            if query == None or query == '':
                return
        else:
            query = actionArgs

        query = query.decode('utf-8')
        database.addSearchHistory(query, 'show')
        query = control.deaccentString(control.display_string(query))
        query = control.quote(query)
        self.showsSearchResults(query)

    def showsSearchResults(self, query):
        query = control.quote_plus(control.unquote(query))
        trakt_list = trakt.json_response('search/show?query=%s&extended=full&type=show&field=title' % query)
        if trakt_list is None:
            return
        self.showListBuilder([show for show in trakt_list if float(show['score']) > 0])
        control.closeAllDialogs()
        control.closeDirectory('tvshows')

    def showsByActor(self, actionArgs):
        if actionArgs == None:
            k = control.showKeyboard('', control.lang(32016))
            k.doModal()
            query = (k.getText() if k.isConfirmed() else None)
            if query == None or query == '':
                return
        else:
            query = control.unquote(actionArgs)

        database.addSearchHistory(query, 'showActor')
        query = control.deaccentString(query)
        query = query.replace(' ', '-')
        query = control.quote_plus(query)

        trakt_list = trakt.json_response('people/%s/shows' % query, limit=True)

        try:
            trakt_list = trakt_list['cast']
        except:
            import traceback
            traceback.print_exc()
            trakt_list = []

        trakt_list = [i['show'] for i in trakt_list]

        self.showListBuilder(trakt_list)

        control.closeDirectory('tvshows')

    def showSeasons(self, args):

        args = control.get_item_information(args)

        self.seasonListBuilder(args['ids']['trakt'])

        control.closeDirectory('seasons')

    def seasonEpisodes(self, args):

        args = control.get_item_information(args)

        show_id = args['showInfo']['ids']['trakt']

        if 'seasonInfo' in args:
            season_number = args['seasonInfo']['info']['season']
        else:
            season_number = args['info']['season']

        self.episodeListBuilder(show_id, season_number)
        control.closeDirectory('episodes', sort='episode')

    def flat_episode_list(self, args):
        args = json.loads(args)
        self.episodeListBuilder(args['trakt_id'])
        control.closeDirectory('episodes')

    def showGenres(self):
        control.addDirectoryItem(control.lang(32065), 'showGenresGet', isFolder=True)
        genres = database.get(trakt.json_response, 24, 'genres/shows')

        if genres is None:
            return

        for i in genres:
            control.addDirectoryItem(i['name'], 'showGenresGet&actionArgs=%s' % i['slug'], isFolder=True)
        control.closeDirectory('addons')

    def showGenreList(self, args, page):
        if page is None:
            page = 1

        if args is None:
            genre_display_list = []
            genre_string = ''
            genres = database.get(trakt.json_response, 24, 'genres/shows')

            for genre in genres:
                genre_display_list.append(genre['name'])
            genre_multiselect = control.showDialog.multiselect("{]: {}".format(control.addonName, control.lang(40298)), genre_display_list)

            if genre_multiselect is None: return
            for selection in genre_multiselect:
                genre_string += ', %s' % genres[selection]['slug']
            genre_string = genre_string[2:]

        else:
            genre_string = args

        page = int(page)
        trakt_list = database.get(trakt.json_response, 12,
                                  'shows/popular?genres=%s&page=%s' % (genre_string, page))
        if trakt_list is None:
            return

        self.showListBuilder(trakt_list)
        control.addDirectoryItem(control.lang(32019),
                               'showGenresGet&actionArgs=%s&page=%s' % (genre_string, page + 1))
        control.closeDirectory('tvshows')

    def showsRelated(self, args):
        trakt_list = database.get(trakt.json_response, 12, 'shows/%s/related' % args)
        if trakt_list is None:
            return

        self.showListBuilder(trakt_list)
        control.closeDirectory('tvshows')

    def showYears(self, year=None, page=None):
        if year is None:
            current_year = int(control.datetime_workaround(datetime.datetime.today().strftime('%Y-%m-%d')).year)
            all_years = reversed([year for year in range(1900, current_year + 1)])
            menu_items = []
            for year in all_years:
                menu_items.append(control.addDirectoryItem(str(year), 'showYears&actionArgs=%s' % year, bulk_add=True))
            control.addMenuItems(syshandle, menu_items, len(menu_items))
            control.closeDirectory('tvshows')
        else:
            if page is None:
                page = 1

            trakt_list = trakt.json_response('shows/popular?years=%s&page=%s' % (year, page))
            self.showListBuilder(trakt_list)
            control.addDirectoryItem(control.lang(32019),
                                   'showYears&actionArgs=%s&page=%s' % (year, int(page) + 1))
            control.closeDirectory('tvshows')

    ######################################################
    # MENU TOOLS
    ######################################################

    def seasonListBuilder(self, show_id, smartPlay=False):

        self.itemList = trakt_database.get_season_list(show_id)

        self.itemList = [x for x in self.itemList if x is not None and 'info' in x]

        self.itemList = sorted(self.itemList, key=lambda k: k['info']['season'])

        if len(self.itemList) == 0:
            control.log('We received no titles to build a list', 'error')
            return

        hide_specials = False

        if control.getSetting('general.hideSpecials') == 'true':
            hide_specials = True

        item_list = []

        for item in self.itemList:
            try:
                if hide_specials and int(item['info']['season']) == 0:
                    continue

                action = 'seasonEpisodes'
                args = {'trakt_id': item['showInfo']['ids']['trakt'],
                        'season': item['info']['season'],
                        'item_type': 'season'}

                args = control.quote(json.dumps(args, sort_keys=True))

                item['trakt_object']['show_id'] = item['showInfo']['ids']['trakt']
                name = item['info']['season_title']

                if not self.is_aired(item['info']) or 'aired' not in item['info']:
                    if control.getSetting('general.hideUnAired') == 'true':
                        continue
                    name = control.colorString(name, 'red')
                    name = control.italic_string(name)
                    item['info']['title'] = name

                item['info'] = control.clean_air_dates(item['info'])

            except:
                import traceback
                traceback.print_exc()
                continue

            if smartPlay is True:
                return args

            item_list.append(control.addDirectoryItem(name, action, item['info'], item['art'], item['cast'], isFolder=True,
                                                    isPlayable=False, actionArgs=args, set_ids=item['ids'],
                                                    bulk_add=True))

        control.addMenuItems(syshandle, item_list, len(item_list))

    def episodeListBuilder(self, show_id, season_number=None, smartPlay=False, hide_unaired=False):

        try:
            item_list = []

            if season_number:
                self.itemList = trakt_database.get_season_episodes(show_id, season_number)
            else:
                self.itemList = trakt_database.get_flat_episode_list(show_id)
                if control.getSetting('general.hideSpecials') == 'true':
                    self.itemList = [i for i in self.itemList if i['info']['season'] != 0]

            self.itemList = [x for x in self.itemList if x is not None and 'info' in x]

            if len(self.itemList) == 0:
                control.log('We received no titles to build a list', 'error')
                return

            if season_number:
                # Building a list of a season, sort by episode
                try:
                    self.itemList = sorted(self.itemList, key=lambda k: k['info']['episode'])
                except:
                    pass
            else:
                # Building a flat list of episodes, sort by season, then episode
                try:
                    self.itemList = sorted(self.itemList, key=lambda k: (k['info']['season'], k['info']['episode']))
                except:
                    pass

            for item in self.itemList:

                try:

                    if control.getSetting('smartplay.playlistcreate') == 'true' and smartPlay is False:
                        action = 'smartPlay'
                        playable = False
                    else:
                        playable = True
                        action = 'getSources'

                    args = {'trakt_id': item['showInfo']['ids']['trakt'],
                            'season': item['info']['season'],
                            'episode': item['info']['episode'],
                            'item_type': 'episode'}

                    args = control.quote(json.dumps(args, sort_keys=True))

                    name = item['info']['title']

                    if not self.is_aired(item['info']):
                        if control.getSetting('general.hideUnAired') == 'true' or hide_unaired:
                            continue
                        else:
                            name = control.colorString(name, 'red')
                            name = control.italic_string(name)
                            item['info']['title'] = name

                    item['info'] = control.clean_air_dates(item['info'])

                except:
                    import traceback
                    traceback.print_exc()
                    continue
                
                item_list.append(control.addDirectoryItem(name, action, item['info'], item['art'], item['cast'], isFolder=False,
                                                        isPlayable=playable, actionArgs=args, bulk_add=True,
                                                        set_ids=item['ids']))

            if smartPlay is True:
                return item_list
            else:
                control.addMenuItems(syshandle, item_list, len(item_list))

        except:
            import traceback
            traceback.print_exc()

    def mixedEpisodeBuilder(self, trakt_list, sort=None, hide_watched=False, smartPlay=False, hide_unaired=True,
                            prepend_date=False):

        try:
            if len(trakt_list) == 0:
                control.log('We received no titles to build a list', 'error')
                return

            self.itemList = trakt_database.get_episode_list(trakt_list)

            self.itemList = [x for x in self.itemList if x is not None and 'info' in x]
            self.itemList = [i for i in self.itemList if 'info' in i and i['info'].get('premiered', None) is not None]
            self.itemList = [i for i in self.itemList if 'info' in i and i['info'].get('premiered', '') is not '']
            if sort is None:
                self.itemList = sorted(self.itemList,
                                       key=lambda i: control.datetime_workaround(i['info']['premiered'],
                                                                               control.trakt_gmt_format, False),
                                       reverse=True)
            elif sort is not False:
                sort_list = []
                for trakt_id in sort['id_list']:
                    try:
                        if not sort['type']:
                            item = [i for i in self.itemList if i['ids']['trakt'] == trakt_id][0]
                        else:
                            item = [i for i in self.itemList if i[sort['type']]['ids']['trakt'] == trakt_id][0]
                        sort_list.append(item)
                    except IndexError:
                        continue
                    except:
                        import traceback
                        traceback.print_exc()
                self.itemList = sort_list

            item_list = []

            for item in self.itemList:
                if item is None:
                    continue

                if item['info'].get('title', '') == '':
                    continue

                if hide_watched and item['info']['playcount'] != 0:
                    continue

                try:
                    name = control.display_string(item['info']['title'])

                    if not self.is_aired(item['info']) and hide_unaired is True:
                        continue
                    elif not self.is_aired(item['info']):
                        name = control.colorString(name, 'red')
                        name = control.italic_string(name)
                        item['info']['title'] = name

                    item['info'] = control.clean_air_dates(item['info'])

                    args = {'trakt_id': item['showInfo']['ids']['trakt'],
                            'season': item['info']['season'],
                            'episode': item['info']['episode'],
                            'item_type': 'episode'}

                    args = control.quote(json.dumps(args, sort_keys=True))

                    if control.getSetting('smartplay.playlistcreate') == 'true' and smartPlay is False:
                        action = 'smartPlay'
                        playable = False
                    else:
                        playable = True
                        action = 'getSources'

                    if self.title_appends == 'true':
                        name = "%s: %sx%s %s" % (control.colorString(item['showInfo']['info']['tvshowtitle']),
                                                 control.display_string(item['info']['season']).zfill(2),
                                                 control.display_string(item['info']['episode']).zfill(2),
                                                 control.display_string(item['info']['title']))
                    if prepend_date:
                        release_day = control.datetime_workaround(item['info']['aired'])
                        release_day = release_day.strftime('%d %b')
                        name = '[%s] %s' % (release_day, name)

                    item['info']['title'] = item['info']['originaltitle'] = name

                    item_list.append(control.addDirectoryItem(name, action, item['info'], item['art'], item['cast'], isFolder=False,
                                                            isPlayable=playable, actionArgs=args, bulk_add=True,
                                                            set_ids=item['ids']))


                except:
                    import traceback
                    traceback.print_exc()
                    continue

            if smartPlay is True:
                return item_list
            else:
                control.addMenuItems(syshandle, item_list, len(item_list))

        except:
            import traceback
            traceback.print_exc()

    def showListBuilder(self, trakt_list, forceResume=False, info_only=False):

        try:
            if len(trakt_list) == 0:
                control.log('We received no titles to build a list', 'error')
                return
        except:
            import traceback
            traceback.print_exc()
            return

        if 'show' in trakt_list[0]:
            trakt_list = [i['show'] for i in trakt_list]

        show_ids = [i['ids']['trakt'] for i in trakt_list]

        self.itemList = trakt_database.get_show_list(show_ids)
        self.itemList = [x for x in self.itemList if x is not None and 'info' in x]
        self.itemList = control.sort_list_items(self.itemList, trakt_list)

        item_list = []

        for item in self.itemList:
            try:
                # Add Arguments to pass with items
                args = {'trakt_id': item['ids']['trakt'], 'item_type': 'show'}
                args = control.quote(json.dumps(args, sort_keys=True))

                name = control.display_string(item['info']['tvshowtitle'])

                if info_only:
                    return args

                if not self.is_aired(item['info']):
                    if control.getSetting('general.hideUnAired') == 'true':
                        continue
                    name = control.colorString(name, 'red')
                    name = control.italic_string(name)

                item['info'] = control.clean_air_dates(item['info'])

                if control.getSetting('smartplay.clickresume') == 'true' or forceResume is True:
                    action = 'playbackResume'
                else:
                    if control.getSetting('general.flatten.episodes') == 'true':
                        action = 'flatEpisodes'
                    else:
                        action = 'showSeasons'

            except:
                import traceback
                traceback.print_exc()
                continue

            item_list.append(control.addDirectoryItem(name, action, item['info'], item['art'], item['cast'], isFolder=True,
                                                    isPlayable=False, actionArgs=args, bulk_add=True,
                                                    set_ids=item['ids']))

        control.addMenuItems(syshandle, item_list, len(item_list))

    def is_aired(self, info):
        try:
            try:
                air_date = info['aired']
            except:
                air_date = info.get('premiered')
            if air_date == '' or air_date is None:
                return False
            if int(air_date[:4]) < 1970:
                return True

            time_format = control.trakt_gmt_format
            if len(air_date) == 10:
                time_format = '%Y-%m-%d'

            air_date = control.gmt_to_local(air_date, format=time_format)

            if control.getSetting('general.datedelay') == 'true':
                air_date = control.datetime_workaround(air_date, time_format, False)
                air_date += datetime.timedelta(days=1)
            else:
                air_date = control.datetime_workaround(air_date, time_format, False)

            if air_date > datetime.datetime.now():
                return False
            else:
                return True
        except:
            import traceback
            traceback.print_exc()
            # Assume an item is not aired if we do not have any information on it or fail to identify
            return False
