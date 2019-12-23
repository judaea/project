import json

from resources.lib.modules import control
from resources.lib.modules import trakt_sync


class TraktSyncDatabase(trakt_sync.TraktSyncDatabase):

    def add_list(self, trakt_id, kodi_meta, name, username, list_type, media_type, updated_at, count, sort_by,
                 sort_how, slug):
        control.traktSyncDB_lock.acquire()
        cursor = self._get_cursor()
        cursor.execute('REPLACE INTO lists ('
                       'trakt_id, kodi_meta, name, username, updated_at, item_count, list_type, media_type, sort_by, '
                       'sort_how, slug) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (int(trakt_id), str(kodi_meta), name, username, updated_at, count, list_type, media_type, sort_by
                        ,sort_how, slug))
        cursor.connection.commit()
        cursor.close()
        control.try_release_lock(control.traktSyncDB_lock)

    def get_lists(self, media_type, list_type):
        control.traktSyncDB_lock.acquire()
        cursor = self._get_cursor()
        cursor.execute('SELECT * FROM lists WHERE list_type=? and media_type=?',
                       (list_type, media_type))
        list = cursor.fetchall()
        cursor.close()
        control.try_release_lock(control.traktSyncDB_lock)
        return list

    def get_list(self, trakt_id, media_type):
        control.traktSyncDB_lock.acquire()
        cursor = self._get_cursor()
        cursor.execute('SELECT * FROM lists WHERE trakt_id=? and media_type=?',
                       (trakt_id, media_type))
        list = cursor.fetchone()
        if list is None:
            cursor.execute('SELECT * FROM lists WHERE slug=? and media_type=?',
                           (trakt_id, media_type))
            list = cursor.fetchone()
        cursor.close()
        control.try_release_lock(control.traktSyncDB_lock)
        return list

    def remove_list(self, trakt_id, media_type):
        control.traktSyncDB_lock.acquire()
        cursor = self._get_cursor()
        cursor.execute('DELETE FROM lists WHERE trakt_id=? AND media_type =?',
                       (trakt_id, media_type))
        cursor.connection.commit()
        cursor.close()
        control.try_release_lock(control.traktSyncDB_lock)
