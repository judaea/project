# -*- coding: utf-8 -*-

import json
import sys


def dispatch(params):
    from resources.lib.modules import control
    from resources.lib.modules import database

    control.SETTINGS_CACHE = {}

    try:

        url = params.get('url')

        action = params.get('action')

        page = params.get('page')

        actionArgs = params.get('actionArgs')

        pack_select = params.get('packSelect')

        source_select = params.get('source_select')

        query = params.get('query')

        judaea_reload = True if params.get('judaea_reload') == 'true' else False

        resume = params.get('resume')

        forceresumeoff = True if params.get('forceresumeoff') == 'true' else False

        forceresumeon = True if params.get('forceresumeon') == 'true' else False

        smartPlay = True if params.get('smartPlay') == 'true' else False

    except:

        print('Welcome to console mode')
        print('Command Help:')
        print('   - Menu Number: opens the relevant menu page')
        print('   - shell: opens a interactive python shell within Judaea')
        print('   - action xxx: run a custom Judaea URL argument')

        url = ''

        action = None

        page = ''

        actionArgs = ''

        pack_select = ''

        source_select = ''

        judaea_reload = ''

        resume = None

        forceresumeoff = True if params.get('forceresumeoff') == 'true' else False

        forceresumeon = True if params.get('forceresumeon') == 'true' else False

        smartPlay = True if params.get('smartPlay') == 'true' else False

    control.log('Judaea, Running Path - Action: %s, actionArgs: %s' % (action, actionArgs))

    if action is None:
        from resources.lib.indexers import navigator

        navigator.Menus().home()

    if action == 'smartPlay':
        from resources.lib.modules import smartPlay
        # if 'resume' not in actionArgs:
        #     actionArgs = json.loads(actionArgs)
        #     actionArgs['resume'] = sys.argv[3].split(':')[-1]
        #     actionArgs = control.quote(json.dumps(actionArgs, sort_keys=True))
        smartPlay.SmartPlay(actionArgs).fill_playlist()

    if action == 'playbackResume':
        from resources.lib.modules import smartPlay
        smart = smartPlay.SmartPlay(actionArgs)
        smart.workaround()

    if action == 'moviesHome':
        from resources.lib.indexers import movies

        movies.Menus().discoverMovies()

    if action == 'moviesPopular':
        from resources.lib.indexers import movies

        movies.Menus().moviesPopular(page)

    if action == 'moviesTrending':
        from resources.lib.indexers import movies

        movies.Menus().moviesTrending(page)

    if action == 'moviesPlayed':
        from resources.lib.indexers import movies

        movies.Menus().moviesPlayed(page)

    if action == 'moviesWatched':
        from resources.lib.indexers import movies

        movies.Menus().moviesWatched(page)

    if action == 'moviesCollected':
        from resources.lib.indexers import movies

        movies.Menus().moviesCollected(page)

    if action == 'moviesAnticipated':
        from resources.lib.indexers import movies

        movies.Menus().moviesAnticipated(page)

    if action == 'moviesBoxOffice':
        from resources.lib.indexers import movies

        movies.Menus().moviesBoxOffice()

    if action == 'moviesUpdated':
        from resources.lib.indexers import movies

        movies.Menus().moviesUpdated(page)

    if action == 'moviesRecommended':
        from resources.lib.indexers import movies

        movies.Menus().moviesRecommended()

    if action == 'moviesSearch':
        from resources.lib.indexers import movies

        movies.Menus().moviesSearch(actionArgs)

    if action == 'moviesSearchResults':
        from resources.lib.indexers import movies

        movies.Menus().moviesSearchResults(actionArgs)

    if action == 'moviesSearchHistory':
        from resources.lib.indexers import movies

        movies.Menus().moviesSearchHistory()

    if action == 'myMovies':
        from resources.lib.indexers import movies

        movies.Menus().myMovies()

    if action == 'moviesMyCollection':
        from resources.lib.indexers import movies

        movies.Menus().myMovieCollection()

    if action == 'moviesMyWatchlist':
        from resources.lib.indexers import movies

        movies.Menus().myMovieWatchlist()

    if action == 'moviesRelated':
        from resources.lib.indexers import movies

        movies.Menus().moviesRelated(actionArgs)

    if action == 'colorPicker':
        control.colorPicker()

    if action == 'authTrakt':
        from resources.lib.modules import trakt

        trakt.TraktAPI().auth()

    if action == 'revokeTrakt':
        from resources.lib.modules import trakt

        trakt.TraktAPI().revokeAuth()

    if action == 'getSources':

        try:

            item_information = control.get_item_information(actionArgs)
            #
            # This tomfoolery here is the new workaround for Judaea to skip the building playlist window

            if control.getSetting('smartplay.playlistcreate') == 'true' or smartPlay:

                if control.playList.size() > 0:
                    playlist_uris = [control.playList[i].getPath() for i in range(control.playList.size())]
                else:
                    playlist_uris = []

                if ('showInfo' in item_information and control.playList.size() == 0) \
                        or not any(sys.argv[2] in i for i in playlist_uris):

                    try:
                        name = item_information['info']['title']
                        item = control.addDirectoryItem(name,
                                                      'getSources',
                                                      item_information['info'],
                                                      item_information['art'],
                                                      item_information['cast'],
                                                      isFolder=False,
                                                      isPlayable=True,
                                                      actionArgs=actionArgs,
                                                      bulk_add=True,
                                                      set_ids=item_information['ids'])
                        control.cancelPlayback()
                        control.playList.add(url=sys.argv[0] + sys.argv[2], listitem=item[1])
                        control.player().play(control.playList)
                        return
                    except:
                        import traceback
                        traceback.print_exc()
                        return

            bookmark_style = control.getSetting('general.bookmarkstyle')

            if control.playList.size() == 1 and resume is not None and bookmark_style != '2' and not forceresumeoff:

                if bookmark_style == '0' and not forceresumeon:
                    import datetime
                    selection = control.showDialog.contextmenu([
                        '{} {}'.format(control.lang(32092), datetime.timedelta(seconds=int(resume))),
                        control.lang(40350)
                    ])
                    if selection == -1:
                        control.cancelPlayback()
                        sys.exit()
                    elif selection != 0:
                        resume = None
            else:
                resume = None

            # Assume if we couldn't get information using the normal method, that it's the legacy method
            if item_information is None:
                item_information = actionArgs

            if not control.premium_check():
                control.showDialog.ok(control.addonName, control.lang(40146), control.lang(40147))
                return None

            if control.playList.getposition() == 0 and control.getSetting('general.scrapedisplay') == '0':
                display_background = True
            else:
                display_background = False

            from resources.lib.modules.skin_manager import SkinManager

            if display_background:
                from resources.lib.modules.windows.persistent_background import PersistentBackground
                background = PersistentBackground(*SkinManager().confirm_skin_path('persistent_background.xml'),
                                                  actionArgs=actionArgs)
                background.setText(control.lang(32045))
                background.show()

            from resources.lib.modules import getSources

            uncached_sources, source_results, args = database.get(getSources.getSourcesHelper,
                                                                  1,
                                                                  actionArgs,
                                                                  judaea_reload=judaea_reload,
                                                                  judaea_sources=True)
            if len(source_results) <= 0:
                control.showDialog.notification(control.addonName, control.lang(32047), time=5000)
                return

            if 'showInfo' in item_information:
                source_select_style = 'Episodes'
            else:
                source_select_style = 'Movie'

            if control.getSetting('general.playstyle%s' % source_select_style) == '1' or source_select == 'true':

                try:
                    background.setText(control.lang(40135))
                except:
                    pass

                from resources.lib.modules import sourceSelect

                stream_link = sourceSelect.sourceSelect(uncached_sources, source_results, actionArgs)

                if stream_link is None:
                    control.showDialog.notification(control.addonName, control.lang(32047), time=5000)
                    raise Exception
                if not stream_link:
                    # user has backed out of source select, don't show no playable sources notification
                    raise Exception
            else:
                try:
                    background.setText(control.lang(32046))
                except:
                    pass

                from resources.lib.modules import resolver

                resolver_window = resolver.Resolver(*SkinManager().confirm_skin_path('resolver.xml'),
                                                    actionArgs=actionArgs)

                stream_link = database.get(resolver_window.doModal, 1,
                                           source_results, args, pack_select,
                                           judaea_reload=judaea_reload)
                del resolver_window

                if stream_link is None:
                    control.closeBusyDialog()
                    control.showDialog.notification(control.addonName, control.lang(32047), time=5000)
                    raise Exception

            control.showBusyDialog()
            try:
                background.close()
            except:
                pass
            try:
                del background
            except:
                pass

            from resources.lib.modules import player

            # if 'resume' not in actionArgs:
            #     actionArgs = json.loads(actionArgs)
            #     actionArgs['resume'] = sys.argv[3].split(':')[-1]
            #     actionArgs = json.dumps(actionArgs, sort_keys=True)

            player.judaeaPlayer().play_source(stream_link, actionArgs, resume_time=resume, params=params)

        except:
            import traceback
            traceback.print_exc()
            # Perform cleanup and make sure all open windows close and playlist is cleared
            try:
                control.closeBusyDialog()
            except:
                pass
            try:
                background.close()
            except:
                pass
            try:
                del background
            except:
                pass
            try:
                resolver_window.close()
            except:
                pass
            try:
                del resolver_window
            except:
                pass
            try:
                control.playList.clear()
            except:
                pass
            try:
                control.closeOkDialog()
            except:
                pass
            try:
                control.cancelPlayback()
            except:
                pass

    if action == 'preScrape':

        from resources.lib.modules.skin_manager import SkinManager

        try:
            item_information = control.get_item_information(actionArgs)

            if 'showInfo' in item_information:
                source_select_style = 'Episodes'
            else:
                source_select_style = 'Movie'

            from resources.lib.modules import getSources

            uncached_sources, source_results, args = database.get(getSources.getSourcesHelper,
                                                                  1,
                                                                  actionArgs,
                                                                  judaea_reload=judaea_reload,
                                                                  judaea_sources=True)

            if control.getSetting('general.playstyle%s' % source_select_style) == '0':
                from resources.lib.modules import resolver

                resolver_window = resolver.Resolver(*SkinManager().confirm_skin_path('resolver.xml'),
                                                                                     actionArgs=actionArgs)
                database.get(resolver_window.doModal, 1, source_results, args, pack_select, judaea_reload=judaea_reload)

            control.setSetting(id='general.tempSilent', value='false')
        except:
            control.setSetting(id='general.tempSilent', value='false')
            import traceback

            traceback.print_exc()
            pass

        control.log('Pre-scraping completed')

    if action == 'authRealDebrid':
        from resources.lib.modules import real_debrid

        real_debrid.RealDebrid().auth()

    if action == 'showsHome':
        from resources.lib.indexers import tvshows

        tvshows.Menus().discoverShows()

    if action == 'myShows':
        from resources.lib.indexers import tvshows

        tvshows.Menus().myShows()

    if action == 'showsMyCollection':
        from resources.lib.indexers import tvshows

        tvshows.Menus().myShowCollection()

    if action == 'showsMyWatchlist':
        from resources.lib.indexers import tvshows

        tvshows.Menus().myShowWatchlist()

    if action == 'showsMyProgress':
        from resources.lib.indexers import tvshows

        tvshows.Menus().myProgress()

    if action == 'showsMyRecentEpisodes':
        from resources.lib.indexers import tvshows

        tvshows.Menus().myRecentEpisodes()

    if action == 'showsPopular':
        from resources.lib.indexers import tvshows

        tvshows.Menus().showsPopular(page)

    if action == 'showsRecommended':
        from resources.lib.indexers import tvshows

        tvshows.Menus().showsRecommended()

    if action == 'showsTrending':
        from resources.lib.indexers import tvshows

        tvshows.Menus().showsTrending(page)

    if action == 'showsPlayed':
        from resources.lib.indexers import tvshows

        tvshows.Menus().showsPlayed(page)

    if action == 'showsWatched':
        from resources.lib.indexers import tvshows

        tvshows.Menus().showsWatched(page)

    if action == 'showsCollected':
        from resources.lib.indexers import tvshows

        tvshows.Menus().showsCollected(page)

    if action == 'showsAnticipated':
        from resources.lib.indexers import tvshows

        tvshows.Menus().showsAnticipated(page)

    if action == 'showsUpdated':
        from resources.lib.indexers import tvshows

        tvshows.Menus().showsUpdated(page)

    if action == 'showsSearch':
        from resources.lib.indexers import tvshows

        tvshows.Menus().showsSearch(actionArgs)

    if action == 'showsSearchResults':
        from resources.lib.indexers import tvshows

        tvshows.Menus().showsSearchResults(actionArgs)

    if action == 'showsSearchHistory':
        from resources.lib.indexers import tvshows

        tvshows.Menus().showSearchHistory()

    if action == 'showSeasons':
        from resources.lib.indexers import tvshows

        tvshows.Menus().showSeasons(actionArgs)

    if action == 'seasonEpisodes':
        from resources.lib.indexers import tvshows

        tvshows.Menus().seasonEpisodes(actionArgs)

    if action == 'showsRelated':
        from resources.lib.indexers import tvshows

        tvshows.Menus().showsRelated(actionArgs)

    if action == 'showYears':
        from resources.lib.indexers import tvshows
        tvshows.Menus().showYears(actionArgs, page)

    if action == 'searchMenu':
        from resources.lib.indexers import navigator

        navigator.Menus().searchMenu()

    if action == 'toolsMenu':
        from resources.lib.indexers import navigator

        navigator.Menus().toolsMenu()

    if action == 'clearCache':
        from resources.lib.modules import control

        control.clearCache()

    if action == 'traktManager':
        from resources.lib.modules import trakt

        trakt.TraktAPI().traktManager(actionArgs)

    if action == 'onDeckShows':
        from resources.lib.indexers import tvshows

        tvshows.Menus().onDeckShows()

    if action == 'onDeckMovies':
        from resources.lib.indexers.movies import Menus

        Menus().onDeckMovies()

    if action == 'cacheAssist':
        from resources.lib.modules import cacheAssist

        cacheAssist.CacheAssit(actionArgs)

    if action == 'tvGenres':
        from resources.lib.indexers import tvshows

        tvshows.Menus().showGenres()

    if action == 'showGenresGet':
        from resources.lib.indexers import tvshows

        tvshows.Menus().showGenreList(actionArgs, page)

    if action == 'movieGenres':
        from resources.lib.indexers import movies

        movies.Menus().movieGenres()

    if action == 'movieGenresGet':
        from resources.lib.indexers import movies

        movies.Menus().movieGenresList(actionArgs, page)

    if action == 'filePicker':
        from resources.lib.modules import smartPlay

        smartPlay.SmartPlay(actionArgs).torrent_file_picker()

    if action == 'shufflePlay':
        from resources.lib.modules import smartPlay

        try:
            smart = smartPlay.SmartPlay(actionArgs).shufflePlay()
        except:
            import traceback
            traceback.print_exc()
            pass

    if action == 'resetSilent':
        control.setSetting('general.tempSilent', 'false')
        control.showDialog.notification('{}: {}'.format(control.addonName, control.lang(40296)), control.lang(32048), time=5000)

    if action == 'clearTorrentCache':
        from resources.lib.modules import database

        database.torrent_cache_clear()

    if action == 'openSettings':
        control.execute('Addon.OpenSettings(%s)' % control.addonInfo('id'))
        control.openSettings(query)

    if action == 'myTraktLists':
        from resources.lib.modules import trakt

        trakt.TraktAPI().myTraktLists(actionArgs)

    if action == 'traktList':
        from resources.lib.modules import trakt

        trakt.TraktAPI().getListItems(actionArgs, page)

    if action == 'nonActiveAssistClear':
        from resources.lib.modules import debridServices

        debridServices.Menus().assist_non_active_clear()

    if action == 'debridServices':
        from resources.lib.modules import debridServices

        debridServices.Menus().home()

    if action == 'cacheAssistStatus':
        from resources.lib.modules import debridServices

        debridServices.Menus().get_assist_torrents()

    if action == 'premiumizeTransfers':
        from resources.lib.modules import debridServices

        debridServices.Menus().list_premiumize_transfers()

    if action == 'showsNextUp':
        from resources.lib.indexers import tvshows

        tvshows.Menus().myNextUp()

    if action == 'runMaintenance':
        from resources.lib.modules import maintenance

        maintenance.run_maintenance()

    if action == 'providerTools':
        from resources.lib.indexers import navigator

        navigator.Menus().providerMenu()

    if action == 'adjustProviders':
        control.log('adjustProviders endpoint has been deprecated')
        return
        # from resources.lib.modules import customProviders
        #
        # customProviders.providers().adjust_providers(actionArgs)

    if action == 'adjustPackage':
        control.log('adjustPackage endpoint has been deprecated')
        return
        # DEPRECATED
        # from resources.lib.modules import customProviders
        #
        # customProviders.providers().adjust_providers(actionArgs, package_disable=True)

    if action == 'installProviders':
        from resources.lib.modules import customProviders

        customProviders.providers().install_package(actionArgs)

    if action == 'uninstallProviders':
        from resources.lib.modules import customProviders

        customProviders.providers().uninstall_package()

    if action == 'showsNew':
        from resources.lib.indexers import tvshows

        tvshows.Menus().newShows()

    if action == 'realdebridTransfers':
        from resources.lib.modules import debridServices

        debridServices.Menus().list_RD_transfers()

    if action == 'cleanInstall':
        from resources.lib.modules import maintenance

        maintenance.wipe_install()

    if action == 'buildPlaylistWorkaround':
        from resources.lib.modules import smartPlay
        smartPlay.SmartPlay(actionArgs).resume_playback()

    if action == 'premiumizeCleanup':
        from resources.lib.modules import maintenance

        maintenance.premiumize_transfer_cleanup()

    if action == 'test2':
        pass

    if action == 'manualProviderUpdate':
        from resources.lib.modules import customProviders

        customProviders.providers().manual_update()

    if action == 'clearSearchHistory':
        from resources.lib.modules import database

        database.clearSearchHistory()

    if action == 'externalProviderInstall':
        from resources.lib.modules import customProviders

        confirmation = control.showDialog.yesno(control.addonName, control.lang(40117))
        if confirmation == 0:
            sys.exit()

        customProviders.providers().install_package(1, url=url)

    if action == 'externalProviderUninstall':
        from resources.lib.modules import customProviders

        confirmation = control.showDialog.yesno(control.addonName, control.lang(40119) % url)
        if confirmation == 0:
            sys.exit()

        customProviders.providers().uninstall_package(package=url, silent=False)

    if action == 'showsNetworks':
        from resources.lib.indexers import tvshows

        tvshows.Menus().showsNetworks()

    if action == 'showsNetworkShows':
        from resources.lib.indexers import tvshows

        tvshows.Menus().showsNetworkShows(actionArgs, page)

    if action == 'movieYears':
        from resources.lib.indexers import movies

        movies.Menus().movieYears()

    if action == 'movieYearsMovies':
        from resources.lib.indexers import movies

        movies.Menus().movieYearsMovies(actionArgs, page)

    if action == 'syncTraktActivities':
        from resources.lib.modules.trakt_sync.activities import TraktSyncDatabase
        TraktSyncDatabase().sync_activities()

    if action == 'traktSyncTools':
        from resources.lib.indexers import navigator
        navigator.Menus().traktSyncTools()

    if action == 'flushTraktActivities':
        from resources.lib.modules import trakt_sync
        trakt_sync.TraktSyncDatabase().flush_activities()

    if action == 'flushTraktDBMeta':
        from resources.lib.modules import trakt_sync
        trakt_sync.TraktSyncDatabase().clear_all_meta()

    if action == 'myfiles':
        from resources.lib.indexers import myfiles
        myfiles.Menus().home()

    if action == 'myfilesFolder':
        from resources.lib.indexers import myfiles
        myfiles.Menus().myfilesFolder(actionArgs)

    if action == 'myfilesPlay':
        from resources.lib.indexers import myfiles
        myfiles.Menus().myfilesPlay(actionArgs)

    if action == 'forceTraktSync':
        from resources.lib.modules import trakt_sync
        from resources.lib.modules.trakt_sync.activities import TraktSyncDatabase
        trakt_sync.TraktSyncDatabase().flush_activities()
        TraktSyncDatabase().sync_activities()

    if action == 'rebuildTraktDatabase':
        from resources.lib.modules.trakt_sync import TraktSyncDatabase
        TraktSyncDatabase().re_build_database()

    if action == 'myUpcomingEpisodes':
        from resources.lib.indexers import tvshows
        tvshows.Menus().myUpcomingEpisodes()

    if action == 'myWatchedEpisodes':
        from resources.lib.indexers import tvshows
        tvshows.Menus().myWatchedEpisodes(page)

    if action == 'myWatchedMovies':
        from resources.lib.indexers import movies
        movies.Menus().myWatchedMovies(page)

    if action == 'showsByActor':
        from resources.lib.indexers import tvshows
        tvshows.Menus().showsByActor(actionArgs)

    if action == 'movieByActor':
        from resources.lib.indexers import movies
        movies.Menus().moviesByActor(actionArgs)

    if action == 'playFromRandomPoint':
        from resources.lib.modules import smartPlay
        smartPlay.SmartPlay(actionArgs).play_from_random_point()

    if action == 'refreshProviders':
        from resources.lib.modules.customProviders import providers
        providers().update_known_providers()

    if action == 'installSkin':
        from resources.lib.modules.skin_manager import SkinManager
        SkinManager().install_skin()

    if action == 'uninstallSkin':
        from resources.lib.modules.skin_manager import SkinManager
        SkinManager().uninstall_skin()

    if action == 'switchSkin':
        from resources.lib.modules.skin_manager import SkinManager
        SkinManager().switch_skin()

    if action == 'manageProviders':
        control.showBusyDialog()
        from resources.lib.modules.windows.custom_providers import CustomProviders
        from resources.lib.modules.skin_manager import SkinManager
        CustomProviders(*SkinManager().confirm_skin_path('custom_providers.xml')).doModal()

    if action == 'flatEpisodes':
        from resources.lib.indexers.tvshows import Menus
        Menus().flat_episode_list(actionArgs)

    if action =='runPlayerDialogs':
        from resources.lib.modules.player import PlayerDialogs
        try:
            PlayerDialogs().display_dialog()
        except:
            import traceback
            traceback.print_exc()

    if action == 'authAllDebrid':
        from resources.lib.modules.all_debrid import AllDebrid
        AllDebrid().auth()

    if action == 'checkSkinUpdates':
        from resources.lib.modules.skin_manager import SkinManager
        SkinManager().check_for_updates()

    if action == 'authPremiumize':
        from resources.lib.modules.premiumize import Premiumize
        Premiumize().auth()