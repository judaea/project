# -*- coding: utf-8 -*-

'''
    David Add-on
    

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


import urlparse,sys,urllib

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

try:
    action = params['action']
except:
    action = None
try:
    name = params['name']
except:
    name = None
try:
    title = params['title']
except:
    title = None
try:
    year = params['year']
except:
    year = None
try:
    imdb = params['imdb']
except:
    imdb = '0'
try:
    tmdb = params['tmdb']
except:
    tmdb = '0'
try:
    tvdb = params['tvdb']
except:
    tvdb = '0'
# try:
#     tvrage = params['tvrage']
# except:
#     tvrage = '0'
try:
    season = params['season']
except:
    season = None
try:
    episode = params['episode']
except:
    episode = None
try:
    tvshowtitle = params['tvshowtitle']
except:
    tvshowtitle = None
try:
    tvshowtitle = params['show']
except:
    pass

premiered = params.get('premiered')

try:
    subid = params['subid']
except:
    subid = None

try:
    docu_category = params['docuCat']
except:
    docu_category = None

try:
    docu_watch = params['docuPlay']
except:
    docu_watch = None

try:
    url = params['url']
except:
    url = None
try:
    image = params['image']
except:
    image = None
try:
    meta = params['meta']
except:
    meta = None

select = params.get('select')

try:
    query = params['query']
except:
    query = None
try:
    source = params['source']
except:
    source = None
try:
    content = params['content']
except:
    content = None

fanart = params.get('fanart')


# if action == None:
#     from resources.lib.indexers import tvshows247
#     tvshows247.indexer().root()
# 
# elif action == 'directory':
#     from resources.lib.indexers import tvshows247
#     tvshows247.indexer().get(url)
# 
# elif action == 'tvtuner':
#     from resources.lib.indexers import tvshows247
#     tvshows247.indexer().tvtuner(url)
# 
# elif action == 'playtvshows247':
#     from resources.lib.indexers import tvshows247
#     tvshows247.player().play(url, content)

if action == None:
    from resources.lib.indexers import navigator
    from resources.lib.modules import cache
    cache.cache_version_check()
    navigator.navigator().root()

if action == 'iptvNavigator':
    from resources.lib.indexers import lists
    lists.indexer().rootIptv()

if action == 'musicNavigator':
    from resources.lib.indexers import lists
    lists.indexer().rootMusic()

if action == 'adultNavigator':
    from resources.lib.indexers import lists
    lists.indexer().rootAdult()

elif action == 'directory':
    from resources.lib.indexers import lists
    lists.indexer().get(url)

elif action == 'qdirectory':
    from resources.lib.indexers import lists
    lists.indexer().getq(url)

elif action == 'xdirectory':
    from resources.lib.indexers import lists
    lists.indexer().getx(url)

elif action == 'developer':
    from resources.lib.indexers import lists
    lists.indexer().developer()

elif action == 'tvtuner':
    from resources.lib.indexers import lists
    lists.indexer().tvtuner(url)

elif 'youtube' in str(action):
    from resources.lib.indexers import lists
    lists.indexer().youtube(url, action)

elif action == 'browser':
    from resources.lib.indexers import lists
    lists.resolver().browser(url)

elif action == 'play':
    from resources.lib.indexers import lists
    if not content == None:
        lists.player().play(url, content)
    else:
        from resources.lib.modules import sources
        sources.sources().play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)

elif action == 'radioNavigator':
    from resources.lib.indexers import radio
    radio.radionet().root()

elif action == 'radio':
    from resources.lib.indexers import radio
    radio.radionet().get_stations(url)

elif action == 'radioCat':
    from resources.lib.indexers import radio
    radio.radionet().get_categories(url)

elif action == 'radioCatStations':
    from resources.lib.indexers import radio
    radio.radionet().get_category_stations(url)

elif action == 'radioPlayStation':
    from resources.lib.indexers import radio
    radio.radionet().play_station(url)

elif action == 'newsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().news()

elif action == 'movieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies()

elif action == 'movieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies(lite=True)

elif action == 'mymovieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies()

elif action == 'mymovieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies(lite=True)

elif action == 'tvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows()

elif action == 'tvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows(lite=True)

elif action == 'mytvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows()

elif action == 'mytvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows(lite=True)

elif action == 'downloadNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().downloads()

elif action == 'toolNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tools()

elif action == 'searchNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().search()

elif action == 'viewsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().views()

elif action == 'clearCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCache()

elif action == 'clearCacheSearch':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheSearch()

elif action == 'clearAllCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheAll()

elif action == 'collectionActors':
    from resources.lib.indexers import navigator
    navigator.navigator().collectionActors()

elif action == 'collectionBoxset':
    from resources.lib.indexers import navigator
    navigator.navigator().collectionBoxset()

elif action == 'collectionBoxsetKids':
    from resources.lib.indexers import navigator
    navigator.navigator().collectionBoxsetKids()

elif action == 'collectionKids':
    from resources.lib.indexers import navigator
    navigator.navigator().collectionKids()

elif action == 'collectionHero':
    from resources.lib.indexers import navigator
    navigator.navigator().collectionHero()

elif action == 'collectionSuperhero':
    from resources.lib.indexers import navigator
    navigator.navigator().collectionSuperhero()

elif action == 'collections':
    from resources.lib.indexers import collections
    collections.collections().get(url)

elif action == 'movies':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'moviePage':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'movieWidget':
    from resources.lib.indexers import movies
    movies.movies().widget()

elif action == 'movieSearch':
    from resources.lib.indexers import movies
    movies.movies().search()

elif action == 'movieSearchnew':
    from resources.lib.indexers import movies
    movies.movies().search_new()

elif action == 'movieSearchterm':
    from resources.lib.indexers import movies
    movies.movies().search_term(name)

elif action == 'moviePerson':
    from resources.lib.indexers import movies
    movies.movies().person()

elif action == 'movieGenres':
    from resources.lib.indexers import movies
    movies.movies().genres()

elif action == 'movieLanguages':
    from resources.lib.indexers import movies
    movies.movies().languages()

elif action == 'movieCertificates':
    from resources.lib.indexers import movies
    movies.movies().certifications()

elif action == 'movieYears':
    from resources.lib.indexers import movies
    movies.movies().years()

elif action == 'moviePersons':
    from resources.lib.indexers import movies
    movies.movies().persons(url)

elif action == 'movieMales':
    from resources.lib.indexers import movies
    movies.movies().males(url)

elif action == 'movieFemales':
    from resources.lib.indexers import movies
    movies.movies().females(url)

elif action == 'movieUserlists':
    from resources.lib.indexers import movies
    movies.movies().userlists()

elif action == 'tvshows':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvshowPage':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvSearch':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search()

elif action == 'tvSearchnew':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search_new()

elif action == 'tvSearchterm':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search_term(name)
    
elif action == 'tvPerson':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().person()

elif action == 'tvGenres':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().genres()

elif action == 'tvNetworks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().networks()

elif action == 'tvLanguages':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().languages()

elif action == 'tvCertificates':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().certifications()

elif action == 'tvPersons':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().persons(url)

elif action == 'tvUserlists':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().userlists()

elif action == 'seasons':
    from resources.lib.indexers import episodes
    episodes.seasons().get(tvshowtitle, year, imdb, tvdb)

elif action == 'episodes':
    from resources.lib.indexers import episodes
    episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, episode)

elif action == 'calendar':
    from resources.lib.indexers import episodes
    episodes.episodes().calendar(url)

elif action == 'tvWidget':
    from resources.lib.indexers import episodes
    episodes.episodes().widget()

elif action == 'calendars':
    from resources.lib.indexers import episodes
    episodes.episodes().calendars()

elif action == 'episodeUserlists':
    from resources.lib.indexers import episodes
    episodes.episodes().userlists()

elif action == 'refresh':
    from resources.lib.modules import control
    control.refresh()

elif action == 'queueItem':
    from resources.lib.modules import control
    control.queueItem()

elif action == 'openSettings':
    from resources.lib.modules import control
    control.openSettings(query)
    
elif action == 'open.Settings.CacheProviders':
    from resources.lib.modules import control
    control.openSettings(query)

elif action == 'artwork':
    from resources.lib.modules import control
    control.artwork()

elif action == 'addView':
    from resources.lib.modules import views
    views.addView(content)

elif action == 'moviePlaycount':
    from resources.lib.modules import playcount
    playcount.movies(imdb, query)

elif action == 'episodePlaycount':
    from resources.lib.modules import playcount
    playcount.episodes(imdb, tvdb, season, episode, query)

elif action == 'tvPlaycount':
    from resources.lib.modules import playcount
    playcount.tvshows(name, imdb, tvdb, season, query)

elif action == 'trailer':
    from resources.lib.modules import trailer
    trailer.trailer().play(name, url)

elif action == 'trailercm':
    from resources.lib.modules import trailercm
    trailercm.trailercm().play(name, url)

elif action == 'traktManager':
    from resources.lib.modules import trakt
    trakt.manager(name, imdb, tvdb, content)

elif action == 'authTrakt':
    from resources.lib.modules import trakt
    trakt.authTrakt()

elif action == 'smuSettings':
    try: import resolveurl
    except: pass
    resolveurl.display_settings()

elif action == 'download':
    import json
    from resources.lib.modules import sources
    from resources.lib.modules import downloader
    try: downloader.download(name, image, sources.sources().sourcesResolve(json.loads(source)[0], True))
    except: pass

elif action == 'docuNavigator':
    from resources.lib.indexers import docu
    if not docu_category == None:
        docu.documentary().docu_list(docu_category)
    elif not docu_watch == None:
        docu.documentary().docu_play(docu_watch)
    else:
        docu.documentary().root()

elif action == 'kidsNavigator':
    from resources.lib.indexers import youtube
    if subid == None:
        youtube.yt_index().root(action)
    else:
        youtube.yt_index().get(action, subid)

# elif action == 'fitness':
#     from resources.lib.indexers import youtube
#     if subid == None:
#         youtube.yt_index().root(action)
#     else:
#         youtube.yt_index().get(action, subid)
# 
# elif action == 'legends':
#     from resources.lib.indexers import youtube
#     if subid == None:
#         youtube.yt_index().root(action)
#     else:
#         youtube.yt_index().get(action, subid)

elif action == 'play':
    from resources.lib.modules import sources
    sources.sources().play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)

elif action == 'addItem':
    from resources.lib.modules import sources
    sources.sources().addItem(title)

elif action == 'playItem':
    from resources.lib.modules import sources
    sources.sources().playItem(title, source)

elif action == 'alterSources':
    from resources.lib.modules import sources
    sources.sources().alterSources(url, meta)

elif action == 'clearSources':
    from resources.lib.modules import sources
    sources.sources().clearSources()

elif action == 'openscrapersSettings':
    from resources.lib.modules import control
    control.openSettings('0.0', 'script.module.openscrapers')

elif action == 'random':
    rtype = params.get('rtype')
    if rtype == 'movie':
        from resources.lib.indexers import movies
        rlist = movies.movies().get(url, create_directory=False)
        r = sys.argv[0]+"?action=play"
    elif rtype == 'episode':
        from resources.lib.indexers import episodes
        rlist = episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, create_directory=False)
        r = sys.argv[0]+"?action=play"
    elif rtype == 'season':
        from resources.lib.indexers import episodes
        rlist = episodes.seasons().get(tvshowtitle, year, imdb, tvdb, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=episode"
    elif rtype == 'show':
        from resources.lib.indexers import tvshows
        rlist = tvshows.tvshows().get(url, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=season"
    from resources.lib.modules import control
    from random import randint
    import json
    try:
        rand = randint(1,len(rlist))-1
        for p in ['title','year','imdb','tvdb','season','episode','tvshowtitle','premiered','select']:
            if rtype == "show" and p == "tvshowtitle":
                try: r += '&'+p+'='+urllib.quote_plus(rlist[rand]['title'])
                except: pass
            else:
                try: r += '&'+p+'='+urllib.quote_plus(rlist[rand][p])
                except: pass
        try: r += '&meta='+urllib.quote_plus(json.dumps(rlist[rand]))
        except: r += '&meta='+urllib.quote_plus("{}")
        if rtype == "movie":
            try: control.infoDialog(rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except: pass
        elif rtype == "episode":
            try: control.infoDialog(rlist[rand]['tvshowtitle']+" - Season "+rlist[rand]['season']+" - "+rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except: pass
        control.execute('RunPlugin(%s)' % r)
    except:
        control.infoDialog(control.lang(32537).encode('utf-8'), time=8000)

