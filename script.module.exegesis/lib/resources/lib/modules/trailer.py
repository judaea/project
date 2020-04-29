# -*- coding: utf-8 -*-

"""
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
"""


import sys
import base64
import json
import random
import re
import urllib

from resources.lib.modules import client
from resources.lib.modules import control


class trailer:
    def __init__(self):
        self.base_link = 'https://www.youtube.com'
        self.youtube = control.addon('plugin.video.youtube').getSetting('youtube.api.key')
        self.key_link = random.choice(['QUl6YVN5QTJVQUF5dm1LZnN0ZDA1aU9tLWltckxUejlCZGJ0aGVF', 'QUl6YVN5QTJVQUF5dm1LZnN0ZDA1aU9tLWltckxUejlCZGJ0aGVF'])

        if self.youtube != '':
            self.key_link = '&key=%s' % self.youtube
        else:
            self.key_link = '&key=%s' % base64.urlsafe_b64decode(self.key_link)
        self.search_link = 'https://www.googleapis.com/youtube/v3/search?part=id&type=video&maxResults=5&q=%s' + self.key_link
        self.youtube_watch = 'https://www.youtube.com/watch?v=%s'


    def play(self, type='', name='', year='', url='', imdb='', windowedtrailer=0):
        try:
            url = self.worker(type, name, year, url, imdb)
            if not url: return

            title = control.infoLabel('ListItem.Title')
            if not title: title = control.infoLabel('ListItem.Label')
            icon = control.infoLabel('ListItem.Icon')

            item = control.item(label=title, iconImage=icon, thumbnailImage=icon, path=url)
            item.setInfo(type="video", infoLabels={'title': title})
            item.setProperty('IsPlayable', 'true')
            control.refresh()
            control.resolve(handle=int(sys.argv[1]), succeeded=True, listitem=item)
            if windowedtrailer == 1:
                control.sleep(1000)
                while control.player.isPlayingVideo():
                    control.sleep(1000)
                control.execute("Dialog.Close(%s, true)" % control.getCurrentDialogId)
        except:
            pass


    def worker(self, type, name, year, url, imdb):
        try:
            if url.startswith(self.base_link):
                url = self.resolve(url)
                if not url: raise Exception()
                return url
            elif not url.startswith('http'):
                url = self.youtube_watch % url
                url = self.resolve(url)
                if not url: raise Exception()
                return url
            else:
                raise Exception()
        except:
            query = name + ' trailer'
            query = self.search_link % urllib.quote_plus(query)
            return self.search(query, type, name, year, imdb)


    def search(self, url, type, name, year, imdb):
        try:
            apiLang = control.apiLanguage().get('youtube', 'en')

            if apiLang != 'en':
                url += "&relevanceLanguage=%s" % apiLang

            result = client.request(url)

            items = json.loads(result).get('items', [])
            items = [i.get('id', {}).get('videoId') for i in items]

            for vid_id in items:
                url = self.resolve(vid_id)
                if url:
                    return url
        except:
            return


    def resolve(self, url):
        try:
            id = url.split('?v=')[-1].split('/')[-1].split('?')[0].split('&')[0]
            result = client.request(self.youtube_watch % id)

            message = client.parseDOM(result, 'div', attrs={'id': 'unavailable-submessage'})
            message = ''.join(message)

            alert = client.parseDOM(result, 'div', attrs={'id': 'watch7-notification-area'})

            if len(alert) > 0: raise Exception()
            if re.search('[a-zA-Z]', message): raise Exception()

            url = 'plugin://plugin.video.youtube/play/?video_id=%s' % id
            return url
        except:
            return
