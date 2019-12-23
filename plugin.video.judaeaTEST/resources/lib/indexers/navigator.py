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

        if trakt:
            control.addDirectoryItem(control.lang(32002), 'myMovies', None, None)

        if trakt:
            control.addDirectoryItem(control.lang(32004), 'myShows', None, None)

        if trakt:
            control.addDirectoryItem('Next Up (Trakt Progress)', 'showsNextUp', None, None)

        control.addDirectoryItem(control.lang(32041), 'toolsMenu')

        control.closeDirectory('addons')


    def toolsMenu(self):

        control.addDirectoryItem('[B]Settings[/B] : Interface', 'openSettings&query=0.0', isFolder=False)
        control.addDirectoryItem('[B]Settings[/B] : Artwork', 'openSettings&query=1.0', isFolder=False)
        control.addDirectoryItem('[B]Settings[/B] : Scraping', 'openSettings&query=2.0', isFolder=False)
        control.addDirectoryItem('[B]Settings[/B] : Playback', 'openSettings&query=3.0', isFolder=False)
        control.addDirectoryItem('[B]Settings[/B] : Accounts', 'openSettings&query=4.0', isFolder=False)
        control.addDirectoryItem('[B]Settings[/B] : Sort & Filter', 'openSettings&query=5.0', isFolder=False)
        control.addDirectoryItem('[B]Settings[/B] : API Keys', 'openSettings&query=6.0', isFolder=False)
        control.addDirectoryItem('[B]Settings[/B] : Clean/Wipe/Sync', 'openSettings&query=7.0', isFolder=False)
        control.addDirectoryItem(control.lang(32042), 'clearCache', isFolder=False)
        control.addDirectoryItem(control.lang(32055), 'clearTorrentCache', isFolder=False)
        control.addDirectoryItem(control.lang(40140), 'clearSearchHistory', isFolder=False)

        control.closeDirectory('addons')


    def traktSyncTools(self):

        control.addDirectoryItem(control.lang(40178), 'flushTraktActivities', None, None, isFolder=False)
        control.addDirectoryItem(control.lang(40179), 'forceTraktSync', None, None, isFolder=False)
        control.addDirectoryItem(control.lang(40180), 'flushTraktDBMeta', None, None, isFolder=False)
        control.addDirectoryItem(control.lang(40181), 'rebuildTraktDatabase', None, None, isFolder=False)

        control.closeDirectory('addons')
