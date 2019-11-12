# -*- coding: utf-8 -*-

import sys
from resources.lib.modules import control
from resources.lib.modules.trakt import TraktAPI
from resources.lib.modules.tmdb import TMDBAPI

try:
    sysaddon = sys.argv[0] ; syshandle = int(sys.argv[1])
except:
    pass

trakt = TraktAPI()
tmdbAPI = TMDBAPI()

class Menus:

    def home(self):
        if control.getSetting('trakt.auth') is not '':
            trakt = True
        else:
            trakt = False

        control.addDirectoryItem(control.lang(32001), 'moviesHome', None, None)
        control.addDirectoryItem(control.lang(32003), 'showsHome', None, None)
#         control.addDirectoryItem('24/7 TV Shows (Trakt Watchlist)', 'showsMyWatchlist', None, None)
#         if trakt:
#             control.addDirectoryItem('24/7 TV Shows (Trakt Watchlist)', 'showsMyWatchlist', None, None)
        if trakt:
            control.addDirectoryItem(control.lang(32002), 'myMovies', None, None)
        if trakt:
            control.addDirectoryItem(control.lang(32004), 'myShows', None, None)
        if trakt:
            control.addDirectoryItem('Next Up (Trakt Progress)', 'showsNextUp', None, None)
        if trakt:
            control.addDirectoryItem('24/7 TV Shows (Trakt Watchlist)', 'showsMyWatchlist', None, None)
#         if control.premiumize_enabled() or control.real_debrid_enabled():
#             control.addDirectoryItem(control.lang(40126), 'myFiles', None, None)
#         control.addDirectoryItem(control.lang(32016), 'searchMenu', None, None)
        control.addDirectoryItem(control.lang(32041), 'toolsMenu')
        # control.addDirectoryItem('Test2', 'test2', None, None, isFolder=True)
        control.closeDirectory('addons')

    def searchMenu(self):

        if control.getSetting('searchHistory') == 'false':
            control.addDirectoryItem(control.lang(32039), 'moviesSearch', isFolder=True, isPlayable=False)
        else:
            control.addDirectoryItem(control.lang(32039), 'moviesSearchHistory')

        if control.getSetting('searchHistory') == 'false':
            control.addDirectoryItem(control.lang(32040), 'showsSearch', isFolder=True, isPlayable=False)
        else:
            control.addDirectoryItem(control.lang(32040), 'showsSearchHistory')
        control.closeDirectory('addons')

    def toolsMenu(self):

#         For adding png images
#         control.addDirectoryItem('[B]Settings[/B] : Interface', 'openSettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png')
        control.addDirectoryItem('[B]Settings[/B] : Interface', 'openSettings&query=0.0', isFolder=False)
        control.addDirectoryItem('[B]Settings[/B] : Artwork', 'openSettings&query=1.0', isFolder=False)
        control.addDirectoryItem('[B]Settings[/B] : Scraping', 'openSettings&query=2.0', isFolder=False)
        control.addDirectoryItem('[B]Settings[/B] : Playback', 'openSettings&query=3.0', isFolder=False)
        control.addDirectoryItem('[B]Settings[/B] : Accounts', 'openSettings&query=4.0', isFolder=False)
        control.addDirectoryItem('[B]Settings[/B] : Sort & Filter', 'openSettings&query=5.0', isFolder=False)
        control.addDirectoryItem('[B]Settings[/B] : API Keys', 'openSettings&query=6.0', isFolder=False)
        control.addDirectoryItem('[B]Settings[/B] : Cache/Wipe/Sync', 'openSettings&query=7.0', isFolder=False)
        control.addDirectoryItem(control.lang(32042), 'clearCache', isFolder=False)
        control.addDirectoryItem(control.lang(32055), 'clearTorrentCache', isFolder=False)
        control.addDirectoryItem(control.lang(40140), 'clearSearchHistory', isFolder=False)

#         control.addDirectoryItem(control.lang(32056), 'openSettings', isFolder=False)
#         control.addDirectoryItem(control.lang(32053), 'providerTools', None, None)

#         if control.getSetting('premiumize.enabled') == 'true' or control.getSetting('realdebrid.enabled') == 'true':
#             control.addDirectoryItem(control.lang(32054), 'debridServices', None, None)

#         control.addDirectoryItem(control.lang(32057), 'cleanInstall', None, None, isFolder=False)
#         control.addDirectoryItem(control.lang(40177), 'traktSyncTools', None, None, isFolder=True)

        control.closeDirectory('addons')

#     def providerMenu(self):
# 
#         control.addDirectoryItem(control.lang(40082), 'manualProviderUpdate', None, None)
#         control.addDirectoryItem(control.lang(40083), 'manageProviders', None, None)
#         control.closeDirectory('addons')

    def traktSyncTools(self):
        control.addDirectoryItem(control.lang(40178), 'flushTraktActivities', None, None, isFolder=False)
        control.addDirectoryItem(control.lang(40179), 'forceTraktSync', None, None, isFolder=False)
        control.addDirectoryItem(control.lang(40180), 'flushTraktDBMeta', None, None, isFolder=False)
        control.addDirectoryItem(control.lang(40181), 'rebuildTraktDatabase', None, None, isFolder=False)
        control.closeDirectory('addons')
