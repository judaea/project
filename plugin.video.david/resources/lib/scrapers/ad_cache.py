# -*- coding: utf-8 -*-
import xbmcaddon, xbmcvfs, xbmcgui
import re
import json
import os
from threading import Thread
from apis.alldebrid_api import AllDebridAPI
from modules import david_cache
from modules.utils import get_release_quality, get_file_info, clean_title, clean_file_name, normalize, supported_video_extensions
from scrapers import build_internal_scrapers_label, label_settings
from modules import settings
# from modules.utils import logger

__addon__ = xbmcaddon.Addon(id='plugin.video.david')
window = xbmcgui.Window(10000)

AllDebrid = AllDebridAPI()
_cache = david_cache.DavidCache()

class AllDebridSource:
    def __init__(self):
        self.scrape_provider = 'ad-cloud'
        self.sources = []
        self.folder_results = []
        self.scrape_results = []

    def results(self, info):
        try:
            self.info = info
            self.db_type = self.info.get("db_type")
            self.title = self.info.get("title")
            self.year = self.info.get("year")
            if self.year: self.rootname = '%s (%s)' % (self.title, self.year)
            else: self.rootname = self.title
            self.season = self.info.get("season", None)
            self.episode = self.info.get("episode", None)
            self.extensions = supported_video_extensions()
            self.folder_query = clean_title(normalize(self.title))
            self.file_query = clean_title(normalize(self.title))
            self.query_list = self._year_query_list() if self.db_type == 'movie' else self._episode_query_list()
            self._scrape_cloud()
            if not self.scrape_results: return self.sources
            self.label_settings = label_settings(self.info['scraper_settings'], self.scrape_provider)
            for item in self.scrape_results:
                try:
                    file_name = normalize(item['name'])
                    file_dl = item['url_link']
                    size = float(int(item['size']))/1073741824
                    video_quality = get_release_quality(file_name)
                    details = get_file_info(file_name)
                    label, multiline_label = build_internal_scrapers_label(self.label_settings, file_name, details, size, video_quality)
                    self.sources.append({'name': file_name,
                                        'label': label,
                                        'multiline_label': multiline_label,
                                        'title': file_name,
                                        'quality': video_quality,
                                        'size': size,
                                        'url_dl': file_dl,
                                        'id': file_dl,
                                        'downloads': False,
                                        'direct': True,
                                        'source': self.scrape_provider,
                                        'scrape_provider': self.scrape_provider})
                except: pass
            window.setProperty('ad-cloud_source_results', json.dumps(self.sources))
        except Exception as e:
            from modules.utils import logger
            logger('DAVID alldebrid scraper Exception', e)
        return self.sources

    def _assigned_content(self, raw_name):
        try:
            string = 'DAVID_AD_%s' % raw_name
            return _cache.get(string)
        except:
            return False

    def _scrape_cloud(self):
        try:
            threads = []
            cloud_files = []
            try: my_cloud_files = AllDebrid.user_cloud()
            except: return self.sources
            try:
                for k, v in my_cloud_files.iteritems():
                    if isinstance(v, dict):
                        cloud_files.append(v)
            except:
                for k, v in my_cloud_files.items():
                    if isinstance(v, dict):
                        cloud_files.append(v)
            my_cloud_files = [i for i in cloud_files if i['statusCode'] == 4]
            for item in my_cloud_files:
                folder_name = clean_title(normalize(item['filename']))
                assigned_content = self._assigned_content(normalize(item['filename']))
                if assigned_content:
                    if assigned_content == self.rootname:
                        self.folder_results.append((normalize(item['filename']), item, True))
                elif self.folder_query in folder_name or not folder_name:
                    self.folder_results.append((normalize(item['filename']), item, False))
            if not self.folder_results: return self.sources
            for i in self.folder_results: threads.append(Thread(target=self._scrape_folders, args=(i,)))
            [i.start() for i in threads]
            [i.join() for i in threads]
        except: pass

    def _scrape_folders(self, folder_info):
        try:
            final_files = []
            extensions = supported_video_extensions()
            assigned_folder = folder_info[2]
            torrent_folder = folder_info[1]
            links = torrent_folder['links']
            total_size = torrent_folder['size']    
            try:
                links_count = len([v for k, v in links.items() if v.lower().endswith(tuple(self.extensions))])
                for k, v in links.items():
                    if v.lower().endswith(tuple(self.extensions)):
                        size = total_size/links_count
                        final_files.append({'name': v, 'url_link': k, 'size': size})
            except:
                links_count = len([v for k, v in links.iteritems() if v.lower().endswith(tuple(self.extensions))])
                for k, v in links.iteritems():
                    if v.lower().endswith(tuple(self.extensions)):
                        size = total_size/links_count
                        final_files.append({'name': v, 'url_link': k, 'size': size})
            for item in final_files:
                filename = clean_title(normalize(item['name']))
                if any(x in filename for x in self.query_list):
                    if assigned_folder:
                        self.scrape_results.append(item)
                    elif self.folder_query in filename:
                        self.scrape_results.append(item)
        except: return

    def _year_query_list(self):
        return [str(self.year), str(int(self.year)+1), str(int(self.year)-1)]

    def _episode_query_list(self):
        return ['s%02de%02d' % (int(self.season), int(self.episode)),
                '%dx%02d' % (int(self.season), int(self.episode)),
                '%02dx%02d' % (int(self.season), int(self.episode)),
                'season%02depisode%02d' % (int(self.season), int(self.episode)),
                'season%depisode%02d' % (int(self.season), int(self.episode)),
                'season%depisode%d' % (int(self.season), int(self.episode))]        



