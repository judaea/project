import xbmc, xbmcgui, xbmcaddon
import sys
import time
from datetime import datetime, timedelta
import _strptime  # fix bug in python import
from modules import settings
# from modules.utils import logger



__addon__ = xbmcaddon.Addon(id='plugin.video.david')
window = xbmcgui.Window(10000)

class VersionCheck:
    def run(self):
        xbmc.log("[DAVID] VersionCheck Service Starting...", 2)
        david_version = __addon__.getAddonInfo('version')
        davidmeta_version = xbmcaddon.Addon(id='script.david.metadata').getAddonInfo('version')
        davidart_version = xbmcaddon.Addon(id='script.david.artwork').getAddonInfo('version')
        xbmc.log("[DAVID] Current DAVID Version: %s" % david_version, 2)
        xbmc.log("[DAVID] Current DAVIDMETA Version: %s" % davidmeta_version, 2)
        xbmc.log("[DAVID] Current DAVIDART Version: %s" % davidart_version, 2)
        xbmc.log("[DAVID] Killing VersionCheck Service", 2)

class CheckSettings:
    def run(self):
        from modules.nav_utils import settings_layout
        xbmc.log("[DAVID] Check Settings Service Starting...", 2)
        settings_layout()
        xbmc.log("[DAVID] Killing Check Settings Service", 2)

class AutoRun:
    def run(self):
        xbmc.log("[DAVID] Autostart Service Starting...", 2)
        if settings.auto_start_david():
            xbmc.log("[DAVID] Killing Autostart Service", 2)
            return xbmc.executebuiltin('RunAddon(plugin.video.david)')
        else: 
            xbmc.log("[DAVID] Killing Autostart Service", 2)
            return

class SubscriptionsUpdater:             
    def run(self):
        xbmc.log("[DAVID] Subscription service starting...")
        hours = settings.subscription_timer()
        while not xbmc.abortRequested:
            if settings.subscription_update():
                try:
                    next_run  = datetime.fromtimestamp(time.mktime(time.strptime(__addon__.getSetting('service_time'), "%Y-%m-%d %H:%M:%S")))
                    now = datetime.now()
                    if now > next_run:
                        if xbmc.Player().isPlaying() == False:
                            if xbmc.getCondVisibility('Library.IsScanningVideo') == False:
                                xbmc.sleep(3000)
                                xbmc.log("[DAVID] Updating video subscriptions")
                                xbmc.executebuiltin('RunPlugin(plugin://plugin.video.david/?&mode=update_subscriptions)')
                                xbmc.sleep(500)
                                if __addon__.getSetting('subsciptions.update_type') == '1':
                                    next_update = datetime.now() + timedelta(hours=24)
                                    next_update = next_update.strftime('%Y-%m-%d') + ' %s:00' % __addon__.getSetting('subscriptions_update_label2')
                                else:
                                    next_update = str(now + timedelta(hours=hours)).split('.')[0]
                                __addon__.setSetting('service_time', next_update)
                                xbmc.sleep(500)
                                xbmc.log("[DAVID] Subscriptions updated. Next run at " + __addon__.getSetting('service_time'), 2)
                                xbmc.sleep(3000)
                        else:
                            xbmc.log("[DAVID] Player is running, waiting until finished")
                except: pass
            xbmc.sleep(3000)

VersionCheck().run()
CheckSettings().run()
AutoRun().run()
SubscriptionsUpdater().run()
