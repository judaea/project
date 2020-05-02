# -*- coding: utf-8 -*-

'''
    Exegesis Add-on

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


# --[ arconaitv v1.0 ]--|--[ From JewBMX ]--
# --[ arconaitv v1.1 ]--|--[ From Tempest ]--
# IPTV Indexer made from the Alberto_Posadas ArconaiTV Plugin.

import os.path, json, requests, re, js2py
import sys, urllib, urlparse
import xbmcaddon, xbmcgui, xbmcplugin, xbmc
from resources.lib.modules import jsunpack, control, client
from bs4 import BeautifulSoup

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
action = args.get('action', None)


class arconaitv:
    def __init__(self):
        self.artbase_url = "https://github.com/judaea/project/blob/master/menus/lists/Arconaitv/%s?raw=true"
        self.arconaitv_url = "https://www.arconaitv.us/"
        self.headers = {'User-Agent': client.agent()}

    def build_url(self, query):
        return base_url + '?' + urllib.urlencode(query)

    def getCableInfo(self, title):
        desc_file = os.path.join(os.path.dirname(__file__), 'cable.json')
        with open(desc_file) as file:
            data = file.read()
        parsed = json.loads(data)
        for cable in parsed['cable']:
            if title == cable['title']:
                return cable
        return {'title': title, 'description': 'New Channel!', 'poster':' DefaultVideo.png'}

    def getShowInfo(self, title):
        desc_file = os.path.join(os.path.dirname(__file__), 'shows.json')
        with open(desc_file) as file:
            data = file.read()
        parsed = json.loads(data)
        for show in parsed['shows']:
            if title == show['title']:
                return show
        return {'title': title, 'description': 'New Show!', 'poster': 'DefaultVideo.png'}

    def getMovieInfo(self, title):
        desc_file = os.path.join(os.path.dirname(__file__), 'movies.json')
        with open(desc_file) as file:
            data = file.read()
        parsed = json.loads(data)
        for movie in parsed['movies']:
            if title == movie['title']:
                return movie
        return {'title': title, 'description': 'New Movie!', 'poster': 'DefaultVideo.png'}

    def listCategories(self):
        url = self.build_url({'action': 'arconai'})
        li = xbmcgui.ListItem("""Please vist https://www.arconaitv.us/ and donate. Anything will help. Thanks""")
        img = self.artbase_url % '247.png'
        li.setArt({'thumb': img, 'poster': img})
        il = {"plot": "Please Help The site get back to normal"}
        li.setInfo(type='Video', infoLabels=il)
        xbmcplugin.addDirectoryItem(addon_handle, url=url, listitem=li, isFolder=False)

        url = self.build_url({'action': 'iptvNavigator'})
        li = xbmcgui.ListItem("Live TV Channels")
        cable_img = self.artbase_url % "livetv.png"
        li.setArt({'thumb': cable_img, 'poster': cable_img})
        il = {"plot": "Live TV Channels"}
        li.setInfo(type='Video', infoLabels=il)
        xbmcplugin.addDirectoryItem(addon_handle, url=url, listitem=li, isFolder=True)

        url = self.build_url({'action': 'tv247Navigator'})
        li = xbmcgui.ListItem("TV Shows")
        shows_img = self.artbase_url % "tvshows-247.png"
        li.setArt({'thumb': shows_img, 'poster': shows_img})
        il = {"plot": "24/7 Tv Shows"}
        li.setInfo(type='Video', infoLabels=il)
        xbmcplugin.addDirectoryItem(addon_handle, url=url, listitem=li, isFolder=True)

        url = self.build_url({'action': 'movies247Navigator'})
        li = xbmcgui.ListItem("Movies")
        movies_img = self.artbase_url % "movies-247.png"
        li.setArt({'thumb': movies_img, 'poster': movies_img})
        il = {"plot": "24/7 Movies"}
        li.setInfo(type='Video', infoLabels=il)
        xbmcplugin.addDirectoryItem(addon_handle, url=url, listitem=li, isFolder=True)

        url = self.build_url({'action': 'randomNavigator', 'selection': 'stream.php?id=random'})
        li = xbmcgui.ListItem("Random Streams")
        movies_img = self.artbase_url % "random-streams.png"
        li.setArt({'thumb': movies_img, 'poster': movies_img})
        il = {"plot": "Streams a Random Channel"}
        li.setProperty('IsPlayable', 'true')
        li.setInfo(type='Video', infoLabels=il)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)

        xbmcplugin.endOfDirectory(addon_handle)

    def iptvChannels(self):
        arconaitv_r = requests.get(urlparse.urljoin(self.arconaitv_url, "index.php"), headers=self.headers)
        html_text = arconaitv_r.text.encode('ascii', 'ignore')
        soup = BeautifulSoup(html_text, 'html.parser')
        try:
            cable = soup.find("div", id="cable")
            boxes = cable.find_all("div", class_="box-content")
        except AttributeError:
            xbmcgui.Dialog().ok("Sorry", "The website has changed or we are downloading from wrong website.")
            return
        listItemlist = []
        for box in boxes:
            if box.a is None:
                continue
            url = self.build_url({'action': 'randomNavigator', 'selection': box.a["href"]})
            title = box.a["title"].strip()
            cableInfo = self.getCableInfo(title)
            li = xbmcgui.ListItem(title, iconImage=cableInfo['poster'])
            il = {"Title": title, "mediatype": "video", "plot": cableInfo['description'], "plotoutline": cableInfo['description']}
            li.setProperty('IsPlayable', 'true')
            li.setInfo(type='Video', infoLabels=il)
            listItemlist.append([url, li, False])
        listLength = len(listItemlist)
        xbmcplugin.addDirectoryItems(addon_handle, items=listItemlist, totalItems=listLength)
        xbmcplugin.setContent(addon_handle, 'tvshows')
        xbmc.executebuiltin("Container.SetViewMode(55)")
        xbmcplugin.endOfDirectory(addon_handle)
        control.idle()

    def Tv247(self):
        arconaitv_r = requests.get(urlparse.urljoin(self.arconaitv_url, "index.php"), headers=self.headers)
        html_text = arconaitv_r.text.encode('ascii', 'ignore')
        soup = BeautifulSoup(html_text, 'html.parser')
        try:
            shows = soup.find("div", id="shows")
            boxes = shows.find_all("div", class_="box-content")
        except AttributeError:
            xbmcgui.Dialog().ok("Sorry", "The website has changed or we are downloading from wrong website.")
            return
        listItemlist = []
        for box in boxes:
            if box.a is None:
                continue
            url = self.build_url({'action': 'randomNavigator', 'selection': box.a["href"]})
            title = box.a["title"].strip()
            showInfo = self.getShowInfo(title)
            li = xbmcgui.ListItem(showInfo['title'], iconImage=showInfo['poster'])
            il = {"Title": title, "mediatype": "video", "plot": showInfo['description'], "plotoutline": showInfo['description']}
            li.setProperty('IsPlayable', 'true')
            li.setInfo(type='Video', infoLabels=il)
            li.setArt({'poster': showInfo['poster'], 'banner': showInfo['poster']})
            listItemlist.append([url, li, False])
        listLength = len(listItemlist)
        xbmcplugin.addDirectoryItems(addon_handle, items=listItemlist, totalItems=listLength)
        xbmcplugin.setContent(addon_handle, 'tvshows')
        xbmcplugin.endOfDirectory(addon_handle)
        xbmc.executebuiltin("Container.SetViewMode(55)")
        control.idle()

    def Movies247(self):
        arconaitv_r = requests.get(urlparse.urljoin(self.arconaitv_url, "index.php"), headers=self.headers)
        html_text = arconaitv_r.text.encode('ascii', 'ignore')
        soup = BeautifulSoup(html_text, 'html.parser')
        try:
            movies = soup.find("div", id="movies")
            boxes = movies.find_all("div", class_="box-content")
        except AttributeError:
            xbmcgui.Dialog().ok("Sorry", "The website has changed or we are downloading from wrong website.")
            return
        listItemlist = []
        for box in boxes:
            if box.a is None:
                continue
            url = self.build_url({'action': 'randomNavigator', 'selection': box.a["href"]})
            title = box.a["title"].strip()
            movieInfo = self.getMovieInfo(title)
            li = xbmcgui.ListItem(movieInfo['title'], iconImage=movieInfo['poster'])
            il = {"Title": title, "mediatype":"video", "plot": movieInfo['description'], "plotoutline": movieInfo['description']}
            li.setProperty('IsPlayable', 'True')
            li.setProperty('mimetype', 'application/x-mpegURL')
            li.setInfo(type='Video', infoLabels=il)
            li.setArt({'poster': movieInfo['poster'], 'banner': movieInfo['poster']})
            listItemlist.append([url, li, False])
        listLength = len(listItemlist)
        xbmcplugin.addDirectoryItems(addon_handle, items=listItemlist, totalItems=listLength)
        xbmcplugin.setContent(addon_handle, 'movies')
        xbmcplugin.endOfDirectory(addon_handle)
        xbmc.executebuiltin("Container.SetViewMode(55)")
        control.idle()

    def playRandom(self, selection):
        url = urlparse.urljoin(self.arconaitv_url, selection)
        url = requests.get(urlparse.urljoin(url, selection), headers=self.headers).content
        url = re.compile("var _(.+?)</script>", re.DOTALL).findall(str(url))[0].strip()
        url = url.replace("eval(", "var a =")
        url = "var _" + url[:-1]
        url = url.replace("decodeURIComponent(escape(r))", "r.slice(305,407)")
        url = js2py.eval_js(url).replace("'", "")
        play_item = xbmcgui.ListItem(path=url + '|User-Agent=%s' % client.agent())
        xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
