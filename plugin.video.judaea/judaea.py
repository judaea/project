# -*- coding: utf-8 -*-

import sys
from resources.lib.modules import control


def api(params):
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

        judaea_reload = params.get('judaea_reload')

        query = params.get('query')


        if judaea_reload == 'true':
            judaea_reload = True

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

    unit_tests = params.get('unit_tests', False)

    if unit_tests:
        control.enable_unit_tests()

    control.log('Judaea, Running Path - Action: %s, actionArgs: %s' % (action, actionArgs))

    if action == None:
        from resources.lib.indexers import homeMenu

        homeMenu.Menus().home()

    if action == 'smartPlay':
        from resources.lib.modules import smartPlay
        smartPlay.SmartPlay(actionArgs).fill_playlist()

    if action == 'playbackResume':
        from resources.lib.modules import smartPlay

        smart = smartPlay.SmartPlay(actionArgs)
        smart.workaround()

    if action == 'moviesHome':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().discoverMovies()

    if action == 'moviesPopular':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().moviesPopular(page)

    if action == 'moviesTrending':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().moviesTrending(page)

    if action == 'moviesPlayed':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().moviesPlayed(page)

    if action == 'moviesWatched':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().moviesWatched(page)

    if action == 'moviesCollected':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().moviesCollected(page)

    if action == 'moviesAnticipated':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().moviesAnticipated(page)

    if action == 'moviesBoxOffice':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().moviesBoxOffice()

    if action == 'moviesUpdated':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().moviesUpdated(page)

    if action == 'moviesRecommended':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().moviesRecommended()

    if action == 'moviesSearch':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().moviesSearch(actionArgs)

    if action == 'moviesSearchResults':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().moviesSearchResults(actionArgs)

    if action == 'moviesSearchHistory':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().moviesSearchHistory()

    if action == 'myMovies':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().myMovies()

    if action == 'moviesMyCollection':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().myMovieCollection()

    if action == 'moviesMyWatchlist':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().myMovieWatchlist()

    if action == 'moviesRelated':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().moviesRelated(actionArgs)

    if action == 'colorPicker':
        control.colorPicker()

    if action == 'authTrakt':
        from resources.lib.modules import trakt

        trakt.TraktAPI().auth()

    if action == 'revokeTrakt':
        from resources.lib.modules import trakt

        trakt.TraktAPI().revokeAuth()

    if action == 'getSources':

        from resources.lib.modules.skin_manager import SkinManager

        try:
            from resources.lib.modules.windows.persistent_background import PersistentBackground
            item_information = control.get_item_information(actionArgs)

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

            if display_background:
                background = PersistentBackground('persistent_background.xml',
                                                  SkinManager().active_skin_path,
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

                resolver_window = resolver.Resolver('resolver.xml',
                                                    SkinManager().active_skin_path,
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

            player.judaeaPlayer().play_source(stream_link, actionArgs)

        except:
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
                sources_window.close()
            except:
                pass
            try:
                del sources_window
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

                from resources.lib.modules import resolver

                resolver_window = resolver.Resolver('resolver.xml', SkinManager().active_skin_path,
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
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().discoverShows()

    if action == 'myShows':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().myShows()

    if action == 'showsMyCollection':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().myShowCollection()

    if action == 'showsMyWatchlist':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().myShowWatchlist()

    if action == 'showsMyProgress':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().myProgress()

    if action == 'showsMyRecentEpisodes':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().myRecentEpisodes()

    if action == 'showsPopular':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().showsPopular(page)

    if action == 'showsRecommended':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().showsRecommended()

    if action == 'showsTrending':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().showsTrending(page)

    if action == 'showsPlayed':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().showsPlayed(page)

    if action == 'showsWatched':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().showsWatched(page)

    if action == 'showsCollected':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().showsCollected(page)

    if action == 'showsAnticipated':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().showsAnticipated(page)

    if action == 'showsUpdated':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().showsUpdated(page)

    if action == 'showsSearch':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().showsSearch(actionArgs)

    if action == 'showsSearchResults':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().showsSearchResults(actionArgs)

    if action == 'showsSearchHistory':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().showSearchHistory()

    if action == 'showSeasons':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().showSeasons(actionArgs)

    if action == 'seasonEpisodes':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().seasonEpisodes(actionArgs)

    if action == 'showsRelated':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().showsRelated(actionArgs)

    if action == 'showYears':
        from resources.lib.indexers import tvshowMenus
        tvshowMenus.Menus().showYears(actionArgs, page)

    if action == 'searchMenu':
        from resources.lib.indexers import homeMenu

        homeMenu.Menus().searchMenu()

    if action == 'toolsMenu':
        from resources.lib.indexers import homeMenu

        homeMenu.Menus().toolsMenu()

    if action == 'clearCache':
        from resources.lib.modules import control

        control.clearCache()

    if action == 'traktManager':
        from resources.lib.modules import trakt

        trakt.TraktAPI().traktManager(actionArgs)

    if action == 'onDeckShows':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().onDeckShows()

    if action == 'onDeckMovies':
        from resources.lib.indexers.movieMenus import Menus

        Menus().onDeckMovies()

    if action == 'cacheAssist':
        from resources.lib.modules import cacheAssist

        cacheAssist.CacheAssit(actionArgs)

    if action == 'tvGenres':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().showGenres()

    if action == 'showGenresGet':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().showGenreList(actionArgs, page)

    if action == 'movieGenres':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().movieGenres()

    if action == 'movieGenresGet':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().movieGenresList(actionArgs, page)

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

#     if action == 'openSettings':
#         control.execute('Addon.OpenSettings(%s)' % control.addonInfo('id'))

    if action == 'openSettings':
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
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().myNextUp()

    if action == 'runMaintenance':
        from resources.lib.modules import maintenance

        maintenance.run_maintenance()

    if action == 'providerTools':
        from resources.lib.indexers import homeMenu

        homeMenu.Menus().providerMenu()

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
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().newShows()

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
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().showsNetworks()

    if action == 'showsNetworkShows':
        from resources.lib.indexers import tvshowMenus

        tvshowMenus.Menus().showsNetworkShows(actionArgs, page)

    if action == 'movieYears':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().movieYears()

    if action == 'movieYearsMovies':
        from resources.lib.indexers import movieMenus

        movieMenus.Menus().movieYearsMovies(actionArgs, page)

    if action == 'syncTraktActivities':
        from resources.lib.modules.trakt_sync.activities import TraktSyncDatabase
        TraktSyncDatabase().sync_activities()

    if action == 'traktSyncTools':
        from resources.lib.indexers import homeMenu
        homeMenu.Menus().traktSyncTools()

    if action == 'flushTraktActivities':
        from resources.lib.modules import trakt_sync
        trakt_sync.TraktSyncDatabase().flush_activities()

    if action == 'flushTraktDBMeta':
        from resources.lib.modules import trakt_sync
        trakt_sync.TraktSyncDatabase().clear_all_meta()

    if action == 'myFiles':
        from resources.lib.indexers import myFiles
        myFiles.Menus().home()

    if action == 'myFilesFolder':
        from resources.lib.indexers import myFiles
        myFiles.Menus().myFilesFolder(actionArgs)

    if action == 'myFilesPlay':
        from resources.lib.indexers import myFiles
        myFiles.Menus().myFilesPlay(actionArgs)

    if action == 'forceTraktSync':
        from resources.lib.modules import trakt_sync
        from resources.lib.modules.trakt_sync.activities import TraktSyncDatabase
        trakt_sync.TraktSyncDatabase().flush_activities()
        TraktSyncDatabase().sync_activities()

    if action == 'rebuildTraktDatabase':
        from resources.lib.modules.trakt_sync import TraktSyncDatabase
        TraktSyncDatabase().re_build_database()

    if action == 'myUpcomingEpisodes':
        from resources.lib.indexers import tvshowMenus
        tvshowMenus.Menus().myUpcomingEpisodes()

    if action == 'showsByActor':
        from resources.lib.indexers import tvshowMenus
        tvshowMenus.Menus().showsByActor(actionArgs)

    if action == 'movieByActor':
        from resources.lib.indexers import movieMenus
        movieMenus.Menus().moviesByActor(actionArgs)

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
        CustomProviders('custom_providers.xml', SkinManager().active_skin_path).doModal()

    if action == 'flatEpisodes':
        from resources.lib.indexers.tvshowMenus import Menus
        Menus().flat_episode_list(actionArgs)

    if unit_tests:
        items = control.xbmcplugin.DIRECTORY.items
        control.xbmcplugin.DIRECTORY.items = []
        return items


if __name__ == "__main__":

    try:
        api_params = dict(control.parse_qsl(sys.argv[2].replace('?', '')))
    except:
        api_params = {}

    api(api_params)
