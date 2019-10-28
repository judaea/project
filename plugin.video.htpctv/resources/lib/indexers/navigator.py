# -*- coding: utf-8 -*-

'''
    htpcTV Add-on
    

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import os,sys,urlparse
import xbmc, xbmcaddon, xbmcgui

from resources.lib.modules import control
from resources.lib.modules import trakt
from resources.lib.modules import cache


sysaddon = sys.argv[0] ; syshandle = int(sys.argv[1]) ; control.moderator()

artPath = control.artPath() ; addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()

traktIndicators = trakt.getTraktIndicatorsInfo()

queueMenu = control.lang(32065).encode('utf-8')


class navigator:
    def getMenuEnabled(self, menu_title):
        is_enabled = control.setting(menu_title).strip()
        if (is_enabled == '' or is_enabled == 'false'):
            return False
        return True


    ADDON_ID      = xbmcaddon.Addon().getAddonInfo('id')
    HOMEPATH      = xbmc.translatePath('special://home/')
    ADDONSPATH    = os.path.join(HOMEPATH, 'addons')
    THISADDONPATH = os.path.join(ADDONSPATH, ADDON_ID)
    LOCALNEWS     = os.path.join(THISADDONPATH, 'news.txt')

    def __init__(self):
        movie_library = os.path.join(control.transPath(control.setting('movie_library')),'')
        tv_library = os.path.join(control.transPath(control.setting('tv_library')),'')
        tv_downloads = os.path.join(control.transPath(control.setting('tv_downloads')),'')
        movie_downloads = os.path.join(control.transPath(control.setting('movie_downloads')),'')

        try:
            if not os.path.exists(movie_library): os.makedirs(movie_library)
        except:
            pass
        try:
            if not os.path.exists(tv_library): os.makedirs(tv_library)
        except:
            pass

    def root(self):
        if self.getMenuEnabled('navi.movies') == True:
            self.addDirectoryItem(32001, 'movieNavigator', 'movies.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.tvShows') == True:
            self.addDirectoryItem(32002, 'tvNavigator', 'tvshows.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvShows247') == True:
            self.addDirectoryItem('24-7 TV Shows', 'tv247Navigator', 'tvshows-247.png', 'DefaultTVShows.png')

        if not control.setting('lists.widget') == '0':
            self.addDirectoryItem(32003, 'mymovieNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')
            self.addDirectoryItem(32004, 'mytvNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')

        if not control.setting('movie.widget') == '0':
            self.addDirectoryItem(32005, 'movieWidget', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png')

        if (traktIndicators == True and not control.setting('tv.widget.alt') == '0') or (traktIndicators == False and not control.setting('tv.widget') == '0'):
            self.addDirectoryItem(32006, 'tvWidget', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png')

        self.addDirectoryItem(32008, 'toolNavigator', 'tools.png', 'DefaultAddonProgram.png')

        downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        if downloads == True:
            self.addDirectoryItem(32009, 'downloadNavigator', 'downloads.png', 'DefaultFolder.png')

        self.addDirectoryItem(32010, 'searchNavigator', 'search.png', 'DefaultFolder.png')

        self.endDirectory()


    def movies(self, lite=False):
        if self.getMenuEnabled('navi.moviesTheaters') == True:
            self.addDirectoryItem(32022, 'movies&url=theaters', 'in-theaters.png', 'DefaultRecentlyAddedMovies.png')
        if self.getMenuEnabled('navi.moviesLatest') == True:
            self.addDirectoryItem(32005, 'movies&url=featured', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png')
        if self.getMenuEnabled('navi.moviesPopular') == True:
            self.addDirectoryItem(32018, 'movies&url=popular', 'most-popular.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviesTrending') == True:
            self.addDirectoryItem(32017, 'movies&url=trending', 'people-watching.png', 'DefaultRecentlyAddedMovies.png')
        if self.getMenuEnabled('navi.moviesGenre') == True:
            self.addDirectoryItem(32011, 'movieGenres', 'genres.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviesMales') == True:
            self.addDirectoryItem('Most Popular Actors', 'movieMales', 'people.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviesFemales') == True:
            self.addDirectoryItem('Most Popular Actresses', 'movieFemales', 'people.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviesActors') == True:
            self.addDirectoryItem('Actor Boxsets', 'collectionActors', 'people-boxsets.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviesBoxsets') == True:
            self.addDirectoryItem('Boxsets', 'collectionBoxset', 'movies-boxsets.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviesCar') == True:
            self.addDirectoryItem('Car Movies', 'collections&url=carmovies', 'car.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviesXmas') == True:
            self.addDirectoryItem('Christmas Movies', 'collections&url=xmasmovies', 'christmas.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviesKids') == True:
            self.addDirectoryItem('Kid Collections', 'collectionKids', 'kids.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviesHero') == True:
            self.addDirectoryItem('Superhero Collections', 'collectionHero', 'superhero.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviesYears') == True:
            self.addDirectoryItem(32012, 'movieYears', 'years.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviesPersons') == True:
            self.addDirectoryItem(32013, 'moviePersons', 'people.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviesLanguages') == True:
            self.addDirectoryItem(32014, 'movieLanguages', 'languages.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviesCertificates') == True:
            self.addDirectoryItem(32015, 'movieCertificates', 'certificates.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviesVoted') == True:
            self.addDirectoryItem(32019, 'movies&url=views', 'most-voted.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviesBoxoffice') == True:
            self.addDirectoryItem(32020, 'movies&url=boxoffice', 'box-office.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviesOscars') == True:
            self.addDirectoryItem(32021, 'movies&url=oscars', 'oscar-winners.png', 'DefaultMovies.png')

        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem(32003, 'mymovieliteNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')

            self.addDirectoryItem(32028, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')

        self.endDirectory()


    def mymovies(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32211, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32211, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)

        elif traktCredentials == True:
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32211, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32211, 'moviesToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(32032, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32033, 'movies&url=imdbwatchlist2', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktCredentials == True:
            self.addDirectoryItem(32035, 'movies&url=traktfeatured', 'trakt.png', 'DefaultMovies.png', queue=True)

        elif imdbCredentials == True:
            self.addDirectoryItem(32035, 'movies&url=featured', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(32036, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)

        self.addDirectoryItem(32039, 'movieUserlists', 'imdb.png', 'DefaultMovies.png')

        if lite == False:
            self.addDirectoryItem(32031, 'movieliteNavigator', 'movies.png', 'DefaultMovies.png')
            self.addDirectoryItem(32028, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')

        self.endDirectory()


    def tvshows(self, lite=False):
        if self.getMenuEnabled('navi.tvPopular') == True:
            self.addDirectoryItem(32018, 'tvshows&url=popular', 'most-popular.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvTrending') == True:
            self.addDirectoryItem(32017, 'tvshows&url=trending', 'people-watching.png', 'DefaultRecentlyAddedEpisodes.png')
        if self.getMenuEnabled('navi.tvGenres') == True:
            self.addDirectoryItem(32011, 'tvGenres', 'genres.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvNetworks') == True:
            self.addDirectoryItem(32016, 'tvNetworks', 'networks.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvLanguages') == True:
            self.addDirectoryItem(32014, 'tvLanguages', 'languages.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvCertificates') == True:
            self.addDirectoryItem(32015, 'tvCertificates', 'certificates.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvRating') == True:
            self.addDirectoryItem(32023, 'tvshows&url=rating', 'highly-rated.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvViews') == True:
            self.addDirectoryItem(32019, 'tvshows&url=views', 'most-voted.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvAiring') == True:
            self.addDirectoryItem(32024, 'tvshows&url=airing', 'airing-today.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvActive') == True:
            self.addDirectoryItem(32025, 'tvshows&url=active', 'returning-tvshows.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvPremier') == True:
            self.addDirectoryItem(32026, 'tvshows&url=premiere', 'new-tvshows.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvAdded') == True:
            self.addDirectoryItem(32006, 'calendar&url=added', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
        if self.getMenuEnabled('navi.tvCalendar') == True:
            self.addDirectoryItem(32027, 'calendars', 'calendar.png', 'DefaultRecentlyAddedEpisodes.png')

        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem(32004, 'mytvliteNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')

            self.addDirectoryItem(32028, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')

        self.endDirectory()


    def mytvshows(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32211, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32211, 'tvshowsToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')

        elif traktCredentials == True:
            self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32211, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32211, 'tvshowsToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(32032, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32033, 'tvshows&url=imdbwatchlist2', 'imdb.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32035, 'tvshows&url=traktfeatured', 'trakt.png', 'DefaultTVShows.png')

        elif imdbCredentials == True:
            self.addDirectoryItem(32035, 'tvshows&url=trending', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
            self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
            self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)

        self.addDirectoryItem(32040, 'tvUserlists', 'imdb.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32041, 'episodeUserlists', 'userlists.png', 'DefaultTVShows.png')

        if lite == False:
            self.addDirectoryItem(32031, 'tvliteNavigator', 'tvshows.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32028, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')

        self.endDirectory()


    def tv247(self):
        self.addDirectoryItem('24-7 TV Shows', 'tv247Navigator', 'tvshows-247.png', 'DefaultTVShows.png')

        self.endDirectory()


    def tools(self):
        self.addDirectoryItem('[B]Settings[/B] : General', 'openSettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Settings[/B] : Navigation', 'openSettings&query=1.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Settings[/B] : Playback', 'openSettings&query=2.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Settings[/B] : Free Accounts', 'openSettings&query=4.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Settings[/B] : Premium Accounts', 'openSettings&query=5.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]htpcTV[/B] : Library', 'libtoolNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]htpcTV[/B] : Viewtypes', 'viewsNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]htpcTV[/B] : Clear Cache', 'clearCache', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]htpcTV[/B] : Clear Search History', 'clearCacheSearch', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]htpcTV[/B] : Clear Provider Sources', 'clearSources', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]htpcTV[/B] : News, Updates & Information', 'newsNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Trakt[/B] : Authorize htpcTV With Trakt', 'authTrakt', 'trakt.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]ResolveURL[/B] : Configure ResolveURL Settings', 'smuSettings', 'tools.png', 'DefaultAddonProgram.png')

        self.endDirectory()


    def library(self):
        self.addDirectoryItem('[B]Library[/B] : Settings', 'openSettings&query=8.0', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem('[B]htpcTV[/B] : Movies Folder', control.setting('movie_library'), 'movies.png', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem('[B]htpcTV[/B] : TV Shows Folder', control.setting('tv_library'), 'tvshows.png', 'DefaultTVShows.png', isAction=False)
        self.addDirectoryItem('[B]htpcTV[/B] : Update Libraries', 'updateLibrary&query=tool', 'library_update.png', 'DefaultAddonProgram.png')

        if trakt.getTraktCredentialsInfo():
            self.addDirectoryItem(32135, 'moviesToLibrary&url=traktcollection', 'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32136, 'moviesToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32137, 'tvshowsToLibrary&url=traktcollection', 'trakt.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32138, 'tvshowsToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png')

        self.endDirectory()


    def downloads(self):
        movie_downloads = control.setting('movie.download.path')
        tv_downloads = control.setting('tv.download.path')

        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(32001, movie_downloads, 'movies.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(32002, tv_downloads, 'tvshows.png', 'DefaultTVShows.png', isAction=False)

        self.endDirectory()


    def search(self):
        self.addDirectoryItem(32001, 'movieSearch', 'search.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvSearch', 'search.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32029, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
        self.addDirectoryItem(32030, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')

        self.endDirectory()


    def views(self):
        try:
            control.idle()

            items = [ (control.lang(32001).encode('utf-8'), 'movies'), (control.lang(32002).encode('utf-8'), 'tvshows'), (control.lang(32054).encode('utf-8'), 'seasons'), (control.lang(32038).encode('utf-8'), 'episodes') ]

            select = control.selectDialog([i[0] for i in items], control.lang(32049).encode('utf-8'))

            if select == -1: return

            content = items[select][1]

            title = control.lang(32059).encode('utf-8')
            url = '%s?action=addView&content=%s' % (sys.argv[0], content)

            poster, banner, fanart = control.addonPoster(), control.addonBanner(), control.addonFanart()

            item = control.item(label=title)
            item.setInfo(type='Video', infoLabels = {'title': title})
            item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'banner': banner})
            item.setProperty('Fanart_Image', fanart)

            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
            control.content(int(sys.argv[1]), content)
            control.directory(int(sys.argv[1]), cacheToDisc=True)

            from resources.lib.modules import cache
            views.setView(content, {})
        except:
            return


    def accountCheck(self):
        if traktCredentials == False and imdbCredentials == False:
            control.idle()
            control.infoDialog(control.lang(32042).encode('utf-8'), sound=True, icon='WARNING')
            sys.exit()


    def infoCheck(self, version):
        try:
            control.infoDialog('', control.lang(32074).encode('utf-8'), time=5000, sound=False)
            return '1'
        except:
            return '1'


    def clearCache(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')


    def clearCacheMeta(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_meta()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')


    def clearCacheProviders(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_providers()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')


    def clearCacheSearch(self):
        control.idle()
        if control.yesnoDialog(control.lang(32056).encode('utf-8'), '', ''):
            control.setSetting('tvsearch', '')
            control.setSetting('moviesearch', '')
            control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')


    def news(self):
            r = open(self.LOCALNEWS)
            compfile = r.read()
            self.showText('News - Updates - Information', compfile)


    def showText(self, heading, text):
        id = 10147
        xbmc.executebuiltin('ActivateWindow(%d)' % id)
        xbmc.sleep(500)
        win = xbmcgui.Window(id)
        retry = 50
        while (retry > 0):
            try:
                xbmc.sleep(10)
                retry -= 1
                win.getControl(1).setLabel(heading)
                win.getControl(5).setText(text)
                quit()
                return
            except: pass


    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try: name = control.lang(name).encode('utf-8')
        except: pass
        url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
        thumb = os.path.join(artPath, thumb) if not artPath == None else icon
        cm = []
        if queue == True: cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if not context == None: cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
    

    def collectionActors(self):
        self.addDirectoryItem('Adam Sandler', 'collections&url=adamsandler', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Al Pacino', 'collections&url=alpacino', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Alan Rickman', 'collections&url=alanrickman', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Anthony Hopkins', 'collections&url=anthonyhopkins', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Angelina Jolie', 'collections&url=angelinajolie', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Arnold Schwarzenegger', 'collections&url=arnoldschwarzenegger', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Charlize Theron', 'collections&url=charlizetheron', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Clint Eastwood', 'collections&url=clinteastwood', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Demi Moore', 'collections&url=demimoore', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Denzel Washington', 'collections&url=denzelwashington', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Eddie Murphy', 'collections&url=eddiemurphy', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Elvis Presley', 'collections&url=elvispresley', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Gene Wilder', 'collections&url=genewilder', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Gerard Butler', 'collections&url=gerardbutler', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Goldie Hawn', 'collections&url=goldiehawn', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jason Statham', 'collections&url=jasonstatham', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jean-Claude Van Damme', 'collections&url=jeanclaudevandamme', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jeffrey Dean Morgan', 'collections&url=jeffreydeanmorgan', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('John Travolta', 'collections&url=johntravolta', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Johnny Depp', 'collections&url=johnnydepp', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Julia Roberts', 'collections&url=juliaroberts', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kevin Costner', 'collections&url=kevincostner', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Liam Neeson', 'collections&url=liamneeson', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mel Gibson', 'collections&url=melgibson', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Melissa McCarthy', 'collections&url=melissamccarthy', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Meryl Streep', 'collections&url=merylstreep', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Michelle Pfeiffer', 'collections&url=michellepfeiffer', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Nicolas Cage', 'collections&url=nicolascage', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Nicole Kidman', 'collections&url=nicolekidman', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Paul Newman', 'collections&url=paulnewman', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Reese Witherspoon', 'collections&url=reesewitherspoon', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Robert De Niro', 'collections&url=robertdeniro', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Samuel L Jackson', 'collections&url=samueljackson', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sean Connery', 'collections&url=seanconnery', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Scarlett Johansson', 'collections&url=scarlettjohansson', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sharon Stone', 'collections&url=sharonstone', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sigourney Weaver', 'collections&url=sigourneyweaver', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Steven Seagal', 'collections&url=stevenseagal', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tom Hanks', 'collections&url=tomhanks', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Vin Diesel', 'collections&url=vindiesel', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Wesley Snipes', 'collections&url=wesleysnipes', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Will Smith', 'collections&url=willsmith', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Winona Ryder', 'collections&url=winonaryder', 'people-boxsets.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()
    

    def collectionBoxset(self):
        self.addDirectoryItem('48 Hrs. (1982-1990)', 'collections&url=fortyeighthours', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ace Ventura (1994-1995)', 'collections&url=aceventura', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Airplane (1980-1982)', 'collections&url=airplane', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Airport (1970-1979)', 'collections&url=airport', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('American Graffiti (1973-1979)', 'collections&url=americangraffiti', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Anaconda (1997-2004)', 'collections&url=anaconda', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Analyze This (1999-2002)', 'collections&url=analyzethis', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Anchorman (2004-2013)', 'collections&url=anchorman', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Austin Powers (1997-2002)', 'collections&url=austinpowers', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Back to the Future (1985-1990)', 'collections&url=backtothefuture', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bad Boys (1995-2003)', 'collections&url=badboys', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bad Santa (2003-2016)', 'collections&url=badsanta', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Basic Instinct (1992-2006)', 'collections&url=basicinstinct', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Beverly Hills Cop (1984-1994)', 'collections&url=beverlyhillscop', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Big Mommas House (2000-2011)', 'collections&url=bigmommashouse', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Blues Brothers (1980-1998)', 'collections&url=bluesbrothers', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bourne (2002-2016)', 'collections&url=bourne', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bruce Almighty (2003-2007)', 'collections&url=brucealmighty', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Caddyshack (1980-1988)', 'collections&url=caddyshack', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cheaper by the Dozen (2003-2005)', 'collections&url=cheaperbythedozen', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cheech and Chong (1978-1984)', 'collections&url=cheechandchong', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Childs Play (1988-2004)', 'collections&url=childsplay', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('City Slickers (1991-1994)', 'collections&url=cityslickers', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Conan (1982-2011)', 'collections&url=conan', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Crank (2006-2009)', 'collections&url=crank', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Crocodile Dundee (1986-2001)', 'collections&url=crodiledunde', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Da Vinci Code (2006-2017)', 'collections&url=davincicode', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Daddy Day Care (2003-2007)', 'collections&url=daddydaycare', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Death Wish (1974-1994)', 'collections&url=deathwish', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Delta Force (1986-1990)', 'collections&url=deltaforce', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Die Hard (1988-2013)', 'collections&url=diehard', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dirty Dancing (1987-2004)', 'collections&url=dirtydancing', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dirty Harry (1971-1988)', 'collections&url=dirtyharry', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dumb and Dumber (1994-2014)', 'collections&url=dumbanddumber', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Escape from New York (1981-1996)', 'collections&url=escapefromnewyork', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Every Which Way But Loose (1978-1980)', 'collections&url=everywhichwaybutloose', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Exorcist (1973-2005)', 'collections&url=exorcist', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Expendables (2010-2014)', 'collections&url=theexpendables', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fast and the Furious (2001-2017)', 'collections&url=fastandthefurious', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Father of the Bride (1991-1995)', 'collections&url=fatherofthebride', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fletch (1985-1989)', 'collections&url=fletch', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Friday (1995-2002)', 'collections&url=friday', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Friday the 13th (1980-2009)', 'collections&url=fridaythe13th', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fugitive (1993-1998)', 'collections&url=fugitive', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('G.I. Joe (2009-2013)', 'collections&url=gijoe', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Get Shorty (1995-2005)', 'collections&url=getshorty', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Gettysburg (1993-2003)', 'collections&url=gettysburg', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ghost Rider (2007-2011)', 'collections&url=ghostrider', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ghostbusters (1984-2016)', 'collections&url=ghostbusters', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Gods Not Dead (2014-2016)', 'collections&url=godsnotdead', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Godfather (1972-1990)', 'collections&url=godfather', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Godzilla (1956-2016)', 'collections&url=godzilla', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Grown Ups (2010-2013)', 'collections&url=grownups', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Grumpy Old Men (2010-2013)', 'collections&url=grumpyoldmen', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Guns of Navarone (1961-1978)', 'collections&url=gunsofnavarone', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Halloween (1978-2009)', 'collections&url=halloween', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hangover (2009-2013)', 'collections&url=hangover', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hannibal Lector (1986-2007)', 'collections&url=hanniballector', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hellraiser (1987-1996)', 'collections&url=hellraiser', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Honey I Shrunk the Kids (1989-1995)', 'collections&url=honeyishrunkthekids', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Horrible Bosses (2011-2014)', 'collections&url=horriblebosses', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hostel (2005-2011)', 'collections&url=hostel', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hot Shots (1991-1996)', 'collections&url=hotshots', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Independence Day (1996-2016)', 'collections&url=independenceday', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Indiana Jones (1981-2008)', 'collections&url=indianajones', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Insidious (2010-2015)', 'collections&url=insidious', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Iron Eagle (1986-1992)', 'collections&url=ironeagle', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jack Reacher (2012-2016)', 'collections&url=jackreacher', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jack Ryan (1990-2014)', 'collections&url=jackryan', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jackass (2002-2013)', 'collections&url=jackass', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('James Bond (1963-2015)', 'collections&url=jamesbond', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jaws (1975-1987)', 'collections&url=jaws', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jeepers Creepers (2001-2017)', 'collections&url=jeeperscreepers', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('John Wick (2014-2017)', 'collections&url=johnwick', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jumanji (1995-2005)', 'collections&url=jumanji', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jurassic Park (1993-2015)', 'collections&url=jurassicpark', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kick-Ass (2010-2013)', 'collections&url=kickass', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kill Bill (2003-2004)', 'collections&url=killbill', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('King Kong (1933-2016)', 'collections&url=kingkong', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lara Croft (2001-2003)', 'collections&url=laracroft', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Legally Blonde (2001-2003)', 'collections&url=legallyblonde', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lethal Weapon (1987-1998)', 'collections&url=leathalweapon', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Look Whos Talking (1989-1993)', 'collections&url=lookwhostalking', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Machete (2010-2013)', 'collections&url=machete', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Magic Mike (2012-2015)', 'collections&url=magicmike', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Major League (1989-1998)', 'collections&url=majorleague', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Man from Snowy River (1982-1988)', 'collections&url=manfromsnowyriver', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mask (1994-2005)', 'collections&url=mask', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Matrix (1999-2003)', 'collections&url=matrix', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Mechanic (2011-2016)', 'collections&url=themechanic', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Meet the Parents (2000-2010)', 'collections&url=meettheparents', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Men in Black (1997-2012)', 'collections&url=meninblack', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mighty Ducks (1995-1996)', 'collections&url=mightyducks', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Miss Congeniality (2000-2005)', 'collections&url=misscongeniality', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Missing in Action (1984-1988)', 'collections&url=missinginaction', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mission Impossible (1996-2015)', 'collections&url=missionimpossible', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Naked Gun (1988-1994)', 'collections&url=nakedgun', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('National Lampoon (1978-2006)', 'collections&url=nationallampoon', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('National Lampoons Vacation (1983-2015)', 'collections&url=nationallampoonsvacation', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('National Treasure (2004-2007)', 'collections&url=nationaltreasure', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Neighbors (2014-2016)', 'collections&url=neighbors', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Night at the Museum (2006-2014)', 'collections&url=nightatthemuseum', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Nightmare on Elm Street (1984-2010)', 'collections&url=nightmareonelmstreet', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Now You See Me (2013-2016)', 'collections&url=nowyouseeme', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Nutty Professor (1996-2000)', 'collections&url=nuttyprofessor', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Oceans Eleven (2001-2007)', 'collections&url=oceanseleven', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Odd Couple (1968-1998)', 'collections&url=oddcouple', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Oh, God (1977-1984)', 'collections&url=ohgod', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Olympus Has Fallen (2013-2016)', 'collections&url=olympushasfallen', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Omen (1976-1981)', 'collections&url=omen', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Paul Blart Mall Cop (2009-2015)', 'collections&url=paulblart', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Pirates of the Caribbean (2003-2017)', 'collections&url=piratesofthecaribbean', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Planet of the Apes (1968-2014)', 'collections&url=planetoftheapes', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Police Academy (1984-1994)', 'collections&url=policeacademy', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Poltergeist (1982-1988)', 'collections&url=postergeist', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Porkys (1981-1985)', 'collections&url=porkys', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Predator (1987-2010)', 'collections&url=predator', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Purge (2013-2016)', 'collections&url=thepurge', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rambo (1982-2008)', 'collections&url=rambo', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('RED (2010-2013)', 'collections&url=red', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Revenge of the Nerds (1984-1987)', 'collections&url=revengeofthenerds', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Riddick (2000-2013)', 'collections&url=riddick', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ride Along (2014-2016)', 'collections&url=ridealong', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Ring (2002-2017)', 'collections&url=thering', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('RoboCop (1987-1993)', 'collections&url=robocop', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rocky (1976-2015)', 'collections&url=rocky', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Romancing the Stone (1984-1985)', 'collections&url=romancingthestone', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rush Hour (1998-2007)', 'collections&url=rushhour', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Santa Clause (1994-2006)', 'collections&url=santaclause', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Saw (2004-2010)', 'collections&url=saw', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sex and the City (2008-2010)', 'collections&url=sexandthecity', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Shaft (1971-2000)', 'collections&url=shaft', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Shanghai Noon (2000-2003)', 'collections&url=shanghainoon', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sin City (2005-2014)', 'collections&url=sincity', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sinister (2012-2015)', 'collections&url=sinister', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sister Act (1995-1993)', 'collections&url=sisteract', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Smokey and the Bandit (1977-1986)', 'collections&url=smokeyandthebandit', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Speed (1994-1997)', 'collections&url=speed', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Stakeout (1987-1993)', 'collections&url=stakeout', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Star Trek (1979-2016)', 'collections&url=startrek', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Star Wars (1977-2015)', 'collections&url=starwars', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Sting (1973-1983)', 'collections&url=thesting', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Taken (2008-2014)', 'collections&url=taken', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Taxi (1998-2007)', 'collections&url=taxi', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ted (2012-2015)', 'collections&url=ted', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Teen Wolf (1985-1987)', 'collections&url=teenwolf', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Terminator (1984-2015)', 'collections&url=terminator', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Terms of Endearment (1983-1996)', 'collections&url=termsofendearment', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Texas Chainsaw Massacre (1974-2013)', 'collections&url=texaschainsawmassacre', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Thing (1982-2011)', 'collections&url=thething', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Thomas Crown Affair (1968-1999)', 'collections&url=thomascrownaffair', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Transporter (2002-2015)', 'collections&url=transporter', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Under Siege (1992-1995)', 'collections&url=undersiege', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Universal Soldier (1992-2012)', 'collections&url=universalsoldier', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Wall Street (1987-2010)', 'collections&url=wallstreet', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Waynes World (1992-1993)', 'collections&url=waynesworld', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Weekend at Bernies (1989-1993)', 'collections&url=weekendatbernies', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Whole Nine Yards (2000-2004)', 'collections&url=wholenineyards', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('X-Files (1998-2008)', 'collections&url=xfiles', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('xXx (2002-2005)', 'collections&url=xxx', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Young Guns (1988-1990)', 'collections&url=youngguns', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Zoolander (2001-2016)', 'collections&url=zoolander', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Zorro (1998-2005)', 'collections&url=zorro', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()


    def collectionKids(self):
        self.addDirectoryItem('Disney Collection', 'collections&url=disneymovies', 'disney.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kids Boxset Collection', 'collectionBoxsetKids', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kids Movie Collection', 'collections&url=kidsmovies', 'kids.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()


    def collectionHero(self):
        self.addDirectoryItem('DC Comics Collection', 'collections&url=dcmovies', 'superhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Marvel Collection', 'collections&url=marvelmovies', 'superhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Superhero Boxsets', 'collectionSuperhero', 'superhero.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()
        

    def collectionBoxsetKids(self):
        self.addDirectoryItem('101 Dalmations (1961-2003)', 'collections&url=onehundredonedalmations', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Addams Family (1991-1998)', 'collections&url=addamsfamily', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Aladdin (1992-1996)', 'collections&url=aladdin', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Alvin and the Chipmunks (2007-2015)', 'collections&url=alvinandthechipmunks', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Atlantis (2001-2003)', 'collections&url=atlantis', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Babe (1995-1998)', 'collections&url=babe', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Balto (1995-1998)', 'collections&url=balto', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bambi (1942-2006)', 'collections&url=bambi', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Beauty and the Beast (1991-2017)', 'collections&url=beautyandthebeast', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Beethoven (1992-2014)', 'collections&url=beethoven', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Brother Bear (2003-2006)', 'collections&url=brotherbear', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cars (2006-2017)', 'collections&url=cars', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cinderella (1950-2007)', 'collections&url=cinderella', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cloudy With a Chance of Meatballs (2009-2013)', 'collections&url=cloudywithachanceofmeatballs', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Despicable Me (2010-2015)', 'collections&url=despicableme', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Finding Nemo (2003-2016)', 'collections&url=findingnemo', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fox and the Hound (1981-2006)', 'collections&url=foxandthehound', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Free Willy (1993-2010)', 'collections&url=freewilly', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ghostbusters (1984-2016)', 'collections&url=ghostbusters', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Gremlins (1984-2016)', 'collections&url=gremlins', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Happy Feet (2006-2011)', 'collections&url=happyfeet', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Harry Potter (2001-2011)', 'collections&url=harrypotter', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Home Alone (1990-2012)', 'collections&url=homealone', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Homeward Bound (1993-1996)', 'collections&url=homewardbound', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Honey, I Shrunk the Kids (1989-1997)', 'collections&url=honeyishrunkthekids', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hotel Transylvania (2012-2015)', 'collections&url=hoteltransylvania', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('How to Train Your Dragon (2010-2014)', 'collections&url=howtotrainyourdragon', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hunchback of Notre Dame (1996-2002)', 'collections&url=hunchbackofnotredame', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ice Age (2002-2016)', 'collections&url=iceage', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jurassic Park (1993-2015)', 'collections&url=jurassicpark', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kung Fu Panda (2008-2016)', 'collections&url=kungfupanda', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lady and the Tramp (1955-2001)', 'collections&url=ladyandthetramp', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lilo and Stitch (2002-2006)', 'collections&url=liloandstitch', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Madagascar (2005-2014)', 'collections&url=madagascar', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Monsters Inc (2001-2013)', 'collections&url=monstersinc', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mulan (1998-2004)', 'collections&url=mulan', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Narnia (2005-2010)', 'collections&url=narnia', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('New Groove (2000-2005)', 'collections&url=newgroove', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Open Season (2006-2015)', 'collections&url=openseason', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Planes (2013-2014)', 'collections&url=planes', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Pocahontas (1995-1998)', 'collections&url=pocahontas', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Problem Child (1990-1995)', 'collections&url=problemchild', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rio (2011-2014)', 'collections&url=rio', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sammys Adventures (2010-2012)', 'collections&url=sammysadventures', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Scooby-Doo (2002-2014)', 'collections&url=scoobydoo', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Short Circuit (1986-1988)', 'collections&url=shortcircuit', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Shrek (2001-2011)', 'collections&url=shrek', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('SpongeBob SquarePants (2004-2017)', 'collections&url=spongebobsquarepants', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Spy Kids (2001-2011)', 'collections&url=spykids', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Star Wars (1977-2015)', 'collections&url=starwars', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Stuart Little (1999-2002)', 'collections&url=stuartlittle', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tarzan (1999-2016)', 'collections&url=tarzan', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Teenage Mutant Ninja Turtles (1978-2009)', 'collections&url=teenagemutantninjaturtles', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Jungle Book (1967-2003)', 'collections&url=thejunglebook', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Karate Kid (1984-2010)', 'collections&url=thekaratekid', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Lion King (1994-2016)', 'collections&url=thelionking', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Little Mermaid (1989-1995)', 'collections&url=thelittlemermaid', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Neverending Story (1984-1994)', 'collections&url=theneverendingstory', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Smurfs (2011-2013)', 'collections&url=thesmurfs', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tooth Fairy (2010-2012)', 'collections&url=toothfairy', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tinker Bell (2008-2014)', 'collections&url=tinkerbell', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tom and Jerry (1992-2013)', 'collections&url=tomandjerry', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Toy Story (1995-2014)', 'collections&url=toystory', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('VeggieTales (2002-2008)', 'collections&url=veggietales', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Winnie the Pooh (2000-2005)', 'collections&url=winniethepooh', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Wizard of Oz (1939-2013)', 'collections&url=wizardofoz', 'kids.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()


    def collectionSuperhero(self):
        self.addDirectoryItem('Avengers (2008-2017)', 'collections&url=avengers', 'superhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Batman (1989-2016)', 'collections&url=batman', 'superhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Captain America (2011-2016)', 'collections&url=captainamerica', 'superhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dark Knight Trilogy (2005-2013)', 'collections&url=darkknight', 'superhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fantastic Four (2005-2015)', 'collections&url=fantasticfour', 'superhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hulk (2003-2008)', 'collections&url=hulk', 'superhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Iron Man (2008-2013)', 'collections&url=ironman', 'superhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Spider-Man (2002-2017)', 'collections&url=spiderman', 'superhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Superman (1978-2016)', 'collections&url=superman', 'superhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('X-Men (2000-2016)', 'collections&url=xmen', 'superhero.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()
        

    def endDirectory(self):
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


