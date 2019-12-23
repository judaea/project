# -*- coding: utf-8 -*-

import time
import requests
import re
import os

from resources.lib.modules import control
from resources.lib.modules import customProviders


def update_themes():
    if control.getSetting('skin.updateAutomatic') == 'true':
        from resources.lib.modules.skin_manager import SkinManager
        SkinManager().check_for_updates(silent=True)

def check_for_addon_update():

    try:
        if control.getSetting('general.checkAddonUpdates') == 'false':
            return
        update_timestamp = float(control.getSetting('addon.updateCheckTimeStamp'))

        if time.time() > (update_timestamp + (24 * (60 * 60))):
            repo_xml = requests.get('https://raw.githubusercontent.com/judaea/judaea/master/packages/addons.xml')
            if not repo_xml.status_code == 200:
                control.log('Could not connect to repo XML, status: %s' % repo_xml.status_code, 'error')
                return
            repo_version = re.findall(r'<addon id=\"plugin.video.judaeaTEST\" version=\"(\d*.\d*.\d*)\"', repo_xml.text)[0]
            local_verison = control.addonVersion
            if control.check_version_numbers(local_verison, repo_version):
                control.showDialog.ok(control.addonName, control.lang(40136) % repo_version)
            control.setSetting('addon.updateCheckTimeStamp', str(time.time()))
    except:
        pass


def update_provider_packages():

    try:
        provider_check_stamp = float(control.getSetting('provider.updateCheckTimeStamp'))
    except:
        import traceback
        traceback.print_exc()
        provider_check_stamp = 0

    if time.time() > (provider_check_stamp + (24 * (60 * 60))):
        if control.getSetting('providers.autoupdates') == 'false':
            available_updates = customProviders.providers().check_for_updates(silent=True, automatic=False)
            if len(available_updates) > 0:
                control.showDialog.notification(control.addonName, control.lang(40239))
        else:
            customProviders.providers().check_for_updates(silent=True, automatic=True)
        control.setSetting('provider.updateCheckTimeStamp', str(time.time()))


def refresh_apis():
    rd_token = control.getSetting('rd.auth')
    rd_expiry = int(float(control.getSetting('rd.expiry')))
    tvdb_token = control.getSetting('tvdb.jw')
    tvdb_expiry = int(float(control.getSetting('tvdb.expiry')))

    try:
        if rd_token != '':
            if time.time() > (rd_expiry - (10 * 60)):
                from resources.lib.modules import real_debrid
                control.log('Service Refreshing Real Debrid Token')
                real_debrid.RealDebrid().refreshToken()
    except:
        pass

    try:
        if tvdb_token != '':
            if time.time() > (tvdb_expiry - (30 * 60)):
                control.log('Service Refreshing TVDB Token')
                from resources.lib.modules import tvdb
                if time.time() > tvdb_expiry:
                    tvdb.TVDBAPI().newToken()
                else:
                    tvdb.TVDBAPI().renewToken()
        else:
            from resources.lib.modules import tvdb
            tvdb.TVDBAPI().newToken()
    except:
        pass


def wipe_install():
    confirm = control.showDialog.yesno(control.addonName, control.lang(33021))
    if confirm == 0:
        return

    confirm = control.showDialog.yesno(control.addonName, control.lang(32049) +
                                     '%s' % control.colorString(control.lang(32050)))
    if confirm == 0:
        return

    import shutil
    import os

#     if os.path.exists(control.dataPath):
#         shutil.rmtree(control.dataPath)
#     os.mkdir(control.dataPath)

    if os.path.exists(control.dataPathScrapers):
        shutil.rmtree(control.dataPathScrapers)
    os.mkdir(control.dataPathScrapers)


def premiumize_transfer_cleanup():
    from resources.lib.modules import premiumize
    from resources.lib.modules import database

    premiumize = premiumize.Premiumize()
    fair_usage = int(premiumize.get_used_space())
    threshold = int(control.getSetting('premiumize.threshold'))

    if fair_usage < threshold:
        control.log('Premiumize Fair Usage below threshold, no cleanup required')
        return
    judaea_transfers = database.get_premiumize_transfers()

    if len(judaea_transfers) == 0:
        control.log('No Premiumize transfers have been created')
        return
    control.log('Premiumize Fair Usage is above threshold, cleaning up Judaea transfers')
    for i in judaea_transfers:
        premiumize.delete_transfer(i['transfer_id'])
        database.remove_premiumize_transfer(i['transfer_id'])


def account_notifications():
    from resources.lib.modules import real_debrid
    from resources.lib.modules import premiumize
    import time

    if control.getSetting('realdebrid.enabled') == 'true':
        premium_status = real_debrid.RealDebrid().get_url('user')['type']
        if premium_status == 'free':
            control.showDialog.notification('%s: Real Debrid' % control.addonName,
                                          control.lang(32051))

    if control.getSetting('premiumize.enabled') == 'true':
        premium_status = premiumize.Premiumize().account_info()['premium_until']
        if time.time() > premium_status:
            control.showDialog.notification('%s: Premiumize' % control.addonName,
                                          control.lang(32052))


def clean_deprecated_settings():

    settings_config_file = os.path.join(control.ADDON_PATH, 'resources', 'settings.xml')
    current_settings_file = os.path.join(control.SETTINGS_PATH)

    valid_settings = []

    with open(settings_config_file, 'r') as config_file:
        for i in config_file.readlines():
            if '<!--' in i:
                continue

            try:
                valid_settings.append(re.findall(r'id="(.*?)"', i)[0])
            except:
                pass

    filtered_settings = []

    with open(current_settings_file, 'r') as settings_file:
        current_setting_lines = settings_file.readlines()

    open_line = current_setting_lines.pop(0)
    closing_line = current_setting_lines.pop(-1)

    for i in current_setting_lines:
        if re.findall(r'id="(.*?)"', i)[0] in valid_settings:
            filtered_settings.append(i)

    if len(valid_settings) != len(filtered_settings):
        control.log('Mismatch in valid settings, cancelling the removal of deprecated settings', 'error')

    with open(current_settings_file, 'w+') as settings_file:
        settings_file.write(open_line)
        for i in filtered_settings:
            settings_file.write(i)
        settings_file.write(closing_line)

    control.log('Filtered settings, removed %s deprecated settings ' %
              (len(current_setting_lines) - len(filtered_settings)))


def run_maintenance():

    control.log('Performing Maintenance')
    # ADD COMMON HOUSE KEEPING ITEMS HERE #

    # Refresh API tokens
    try:
        refresh_apis()
    except:
        pass

    # Check cloud account status and alert user if expired
    try:
        if control.getSetting('general.accountNotifications') == 'true':
            account_notifications()
    except:
        pass

    # Deploy the init.py file for the providers folder and make sure it's refreshed on startup
    try:
        customProviders.providers().deploy_init()
    except:
        pass

    try:
        update_provider_packages()
    except:
        pass

    try:
        update_themes()
    except:
        pass

    # Check Premiumize Fair Usage for cleanup
    try:
        if control.getSetting('premiumize.enabled') == 'true' and control.getSetting('premiumize.autodelete') == 'true':
            premiumize_transfer_cleanup()
    except:
        pass

    try:
        clean_deprecated_settings()
    except:
        import traceback
        traceback.print_exc()