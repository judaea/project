# -*- coding: utf-8 -*-

import sys
try: from urlparse import parse_qsl
except ImportError: from urllib.parse import parse_qsl

params = dict(parse_qsl(sys.argv[2].replace('?', '')))
mode = params.get('mode')

if mode == 'clear_cache':
	import davidmeta
	davidmeta.delete_meta_cache()
elif mode == 'set_language':
	import davidmeta
	davidmeta.choose_language()
elif mode == 'clear_tvdb_token':
	from davidmeta.utils import clear_tvdb_token
	clear_tvdb_token()