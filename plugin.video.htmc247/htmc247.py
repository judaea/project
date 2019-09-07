# -*- coding: utf-8 -*-

'''
    htmc247 Add-on
    Copyright (C) 2016 htmc247

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
    url = params['url']
except:
    url = None

try:
    content = params['content']
except:
    content = None

fanart = params.get('fanart')


if action == None:
    from resources.lib.indexers import tvshows247
    tvshows247.indexer().root()

elif action == 'directory':
    from resources.lib.indexers import tvshows247
    tvshows247.indexer().get(url)

elif action == 'tvtuner':
    from resources.lib.indexers import tvshows247
    tvshows247.indexer().tvtuner(url)

elif action == 'playtvshows247':
    from resources.lib.indexers import tvshows247
    tvshows247.player().play(url, content)
