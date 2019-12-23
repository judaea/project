# -*- coding: utf-8 -*-

import xbmc

from resources.lib.modules import maintenance
from resources.lib.modules import control
from resources.lib.modules.trakt_sync.activities import TraktSyncDatabase

control.log('##################  STARTING SERVICE  ######################')
monitor = xbmc.Monitor()

control.setSetting('general.tempSilent', 'false')

control.log('Performing initial background maintenance...')

if control.getSetting('general.checkAddonUpdates') == 'true':
    maintenance.check_for_addon_update()

TraktSyncDatabase().sync_activities()

maintenance.run_maintenance()

control.log('Initial maintenance cycle completed')

control.log('#############  SERVICE ENTERED KEEP ALIVE  #################')

while not monitor.abortRequested():
    try:
        if monitor.waitForAbort(60 * 15):
            break
        control.execute('RunPlugin("plugin://plugin.video.%s/?action=runMaintenance")' % control.addonName.lower())
        TraktSyncDatabase().sync_activities()
    except:
        continue


