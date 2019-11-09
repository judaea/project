# -*- coding: utf-8 -*-

import os
import xbmc

from resources.lib.modules import maintenance
from resources.lib.modules import control
from resources.lib.modules.trakt_sync.activities import TraktSyncDatabase

control.log('##################  STARTING SERVICE  ######################')

control.setSetting('general.tempSilent', 'false')
control.log('Checking Common API Tokens for refresh')
if control.getSetting('general.checkAddonUpdates') == 'true':
    maintenance.check_for_addon_update()
maintenance.run_maintenance()
control.log('Initial API Checks have completed succesfully')
monitor = xbmc.Monitor()
control.log('#############  SERVICE ENTERED KEEP ALIVE  #################')
TraktSyncDatabase().sync_activities()

while not monitor.abortRequested():
    try:
        if monitor.waitForAbort(60 * 15):
            break
        control.execute('RunPlugin("plugin://plugin.video.%s/?action=runMaintenance")' % control.addonName.lower())
        TraktSyncDatabase().sync_activities()
    except:
        continue


