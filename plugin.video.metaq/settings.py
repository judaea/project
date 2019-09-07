#! /usr/bin/python
CACHE_TTL = 60
#UPDATE_LIBRARY_INTERVAL = 4*60*60

if __name__ == "__main__":
    import xml.etree.ElementTree as ET
    tree = ET.parse('resources/settings.xml')
    ids = filter(None, [item.get('id') for item in tree.findall('.//setting')])
    content = []
    with open(__file__, "r") as me:
        content = me.readlines()
        content = content[:content.index("#GENERATED\n")+1]
    with open(__file__, 'w') as f:
        f.writelines(content)
        for _id in ids:
            line = "SETTING_{0} = \"{1}\"\n".format(_id.upper(), _id)
            f.write(line)    

#GENERATED
SETTING_LIBRARY_UPDATES = "library_updates"
SETTING_LIBRARY_SET_DATE = "library_set_date"
SETTING_LIBRARY_SYNC_COLLECTION = "library_sync_collection"
SETTING_LIBRARY_SYNC_WATCHLIST = "library_sync_watchlist"
SETTING_UPDATE_LIBRARY_INTERVAL = "update_library_interval"
SETTING_AIRED_UNKNOWN = "aired_unknown"
SETTING_LIBRARY_TAGS = "library_tags"
SETTING_AIRDATE_OFFSET = "airdate_offset"
SETTING_INCLUDE_SPECIALS = "include_specials"
SETTING_TOTAL_SETUP_DONE = "total_setup_done"
SETTING_PLAYERS_UPDATE_URL = "players_update_url"
SETTING_TRAKT_ACCESS_TOKEN = "trakt_access_token"
SETTING_TRAKT_REFRESH_TOKEN = "trakt_refresh_token"
SETTING_TRAKT_EXPIRES_AT = "trakt_expires_at"
SETTING_MOVIES_ENABLED_PLAYERS = "movies_enabled_players"
SETTING_MOVIES_DEFAULT_PLAYER = "movies_default_player"
SETTING_MOVIES_DEFAULT_PLAYER_FROM_LIBRARY = "movies_default_player_from_library"
SETTING_MOVIES_DEFAULT_PLAYER_FROM_CONTEXT = "movies_default_player_from_context"
SETTING_MOVIES_LIBRARY_FOLDER = "movies_library_folder"
SETTING_MOVIES_PLAYLIST_FOLDER = "movies_playlist_folder"
SETTING_MOVIES_DEFAULT_AUTO_ADD = "movies_default_auto_add"
SETTING_MOVIES_PLAYED_BY_ADD = "movies_played_by_add"
SETTING_MOVIES_BATCH_ADD_FILE_PATH = "movies_batch_add_file_path"
SETTING_TV_ENABLED_PLAYERS = "tv_enabled_players"
SETTING_TV_DEFAULT_PLAYER = "tv_default_player"
SETTING_TV_DEFAULT_PLAYER_FROM_LIBRARY = "tv_default_player_from_library"
SETTING_TV_DEFAULT_PLAYER_FROM_CONTEXT = "tv_default_player_from_context"
SETTING_TV_LIBRARY_FOLDER = "tv_library_folder"
SETTING_TV_PLAYLIST_FOLDER = "tv_playlist_folder"
SETTING_TV_DEFAULT_AUTO_ADD = "tv_default_auto_add"
SETTING_TV_PLAYED_BY_ADD = "tv_played_by_add"
SETTING_TV_BATCH_ADD_FILE_PATH = "tv_batch_add_file_path"
SETTING_PREFERRED_TOGGLE = "preferred_toggle"
SETTING_PRIMARY_SKIN = "primary_skin"
SETTING_ALTERNATE_SKIN = "alternate_skin"
SETTING_RANDOM_PAGES = "random_pages"
SETTING_USE_SIMPLE_SELECTOR = "use_simple_selector"
SETTING_AUTO_HIDE_DIALOGS = "auto_hide_dialogs"
SETTING_AUTO_HIDE_DIALOGS_PROGRESS = "auto_hide_dialogs_progress"
SETTING_AUTO_HIDE_DIALOGS_INFO = "auto_hide_dialogs_info"
SETTING_AUTO_HIDE_DIALOGS_KEYBOARD = "auto_hide_dialogs_keyboard"
SETTING_POOL_SIZE = "pool_size"
SETTING_STYLE = "style"
SETTING_STYLE_CUSTOM_FOLDER = "style_custom_folder"
SETTING_BACKGROUND = "background"
SETTING_BACKGROUND_CUSTOM_FOLDER = "background_custom_folder"
SETTING_LANGUAGE_ID = "language_id"
SETTING_TRAKT_LIST_ARTWORK = "trakt_list_artwork"
SETTING_TRAKT_PERIOD = "trakt_period"
SETTING_ITEMS_PER_PAGE = "items_per_page"
SETTING_FORCE_VIEW = "force_view"
SETTING_MAIN_VIEW = "main_view"
SETTING_MOVIES_VIEW = "movies_view"
SETTING_TVSHOWS_VIEW = "tvshows_view"
SETTING_SEASONS_VIEW = "seasons_view"
SETTING_EPISODES_VIEW = "episodes_view"
SETTING_LIST_VIEW = "list_view"
SETTING_MOVIES_ENABLED_CHANNELERS = "movies_enabled_channelers"
SETTING_MOVIES_DEFAULT_CHANNELER = "movies_default_channeler"
SETTING_TV_ENABLED_CHANNELERS = "tv_enabled_channelers"
SETTING_TV_DEFAULT_CHANNELER = "tv_default_channeler"
SETTING_LIBRARY_TITLES = "library_titles"
SETTING_SYNC_FOLDER = "sync_folder"
SETTING_AUTOPATCH = "autopatch"
SETTING_AUTOPATCHES = "autopatches"
SETTING_TRAKT_API_CLIENT_ID = "trakt_api_client_id"
SETTING_TRAKT_API_CLIENT_SECRET = "trakt_api_client_secret"
SETTING_TMDB_API = "tmdb_api"
SETTING_TVDB_API = "tvdb_api"
