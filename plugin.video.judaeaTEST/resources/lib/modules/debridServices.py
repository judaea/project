# -*- coding: utf-8 -*-

from resources.lib.modules import database
from resources.lib.modules import control


class Menus:

    def __init__(self):
        self.view_type = 'addons'

    def home(self):
        control.addDirectoryItem(control.lang(40182), 'cacheAssistStatus', None, None)
        if control.getSetting('premiumize.enabled') == 'true':
            control.addDirectoryItem(control.lang(40183), 'premiumizeTransfers', None, None)
        if control.getSetting('realdebrid.enabled') == 'true':
            control.addDirectoryItem(control.lang(40184), 'realdebridTransfers', None, None)
        control.closeDirectory(self.view_type)

    def get_assist_torrents(self):
        control.addDirectoryItem(control.lang(40185), 'nonActiveAssistClear', None, None)
        torrent_list = database.get_assist_torrents()
        if torrent_list is not None:

            for i in torrent_list:
                debrid = control.shortened_debrid(i['provider'])
                title = control.colorString('%s - %s - %s%% : %s' % (debrid, i['status'].title(),
                                                                 i['progress'], i['release_title']))
                control.addDirectoryItem(title, '', None, None)

        control.closeDirectory(self.view_type)

    def assist_non_active_clear(self):
        database.clear_non_active_assist()

    def list_premiumize_transfers(self):

        from resources.lib.modules import premiumize
        transfer_list = premiumize.Premiumize().list_transfers()
        if len(transfer_list['transfers']) == 0 or 'transfers' not in transfer_list:
            control.closeDirectory(self.view_type)
            return
        for i in transfer_list['transfers']:
            title = '%s - %s%% : %s' % \
                    (control.colorString(i['status'].title()), str(i['progress'] * 100), i['name'][:50] + "...")
            control.addDirectoryItem(title, '', None, None, isPlayable=False, isFolder=False, isAction=True)
        control.closeDirectory(self.view_type)

    def list_RD_transfers(self):

        from resources.lib.modules import real_debrid
        transfer_list = real_debrid.RealDebrid().list_torrents()
        if len(transfer_list) == 0:
            control.closeDirectory(self.view_type)
            return
        for i in transfer_list:
            title = '%s - %s%% : %s' % \
                    (control.colorString(i['status'].title()), str(i['progress']), i['filename'][:50] + "...")
            control.addDirectoryItem(title, '', None, None, isPlayable=False, isFolder=False, isAction=True)
        control.closeDirectory(self.view_type)