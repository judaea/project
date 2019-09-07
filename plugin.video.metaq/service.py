#!/usr/bin/python
# -*- coding: utf-8 -*-
if __name__ == '__main__':
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'lib'))

import datetime
import glob
import re
import sqlite3
import xbmcgui
import xbmc

from xbmcswift2 import xbmc, xbmcvfs
from meta import plugin
from meta.video_player import VideoPlayer
from meta.utils.properties import get_property, clear_property
from default import update_library
from settings import SETTING_UPDATE_LIBRARY_INTERVAL, SETTING_TOTAL_SETUP_DONE
from language import get_string as _

player = VideoPlayer()

class Monitor(xbmc.Monitor):
    def onDatabaseUpdated(self, database):
        if database == "video":
            if get_property("clean_library"):
                xbmc.executebuiltin("XBMC.CleanLibrary(video, false)")
                clear_property("clean_library")
                
monitor = Monitor()

def go_idle(duration):
    while not xbmc.abortRequested and duration > 0:
        if player.isPlayingVideo():
            player.currentTime = player.getTime()
        xbmc.sleep(1000)
        duration -= 1

def future(seconds):
    return datetime.datetime.now() + datetime.timedelta(seconds=seconds)

def main():
    go_idle(15)
    if plugin.get_setting(SETTING_TOTAL_SETUP_DONE, bool) == False:
        xbmc.executebuiltin('RunPlugin(plugin://plugin.video.metaq/setup/total)')
        plugin.set_setting(SETTING_TOTAL_SETUP_DONE, "true")
    xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metaq/movies/batch_add_to_library)")
    next_update = future(0)
    while not xbmc.abortRequested:
        if next_update <= future(0):
            next_update = future(plugin.get_setting(SETTING_UPDATE_LIBRARY_INTERVAL, int) * 60 * 60)
            update_library()
        go_idle(30*60)

if __name__ == '__main__':
    main()