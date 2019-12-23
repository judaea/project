from resources.lib.modules import control
from resources.lib.modules import trakt_sync


class TraktSyncDatabase(trakt_sync.TraktSyncDatabase):

    def get_bookmark(self, trakt_id):
        control.traktSyncDB_lock.acquire()
        try:
            cursor = self._get_cursor()
            cursor.execute("SELECT * FROM bookmark WHERE trakt_id =?", (trakt_id,))
            return cursor.fetchone()
        except:
            import traceback
            traceback.print_exc()
        finally:
            control.try_release_lock(control.traktSyncDB_lock)
            try:
                cursor.close()
            except:
                pass

    def set_bookmark(self, trakt_id, time_in_seconds):
        control.traktSyncDB_lock.acquire()
        try:
            time_in_seconds = int(time_in_seconds)
            cursor = self._get_cursor()
            cursor.execute("REPLACE INTO bookmark VALUES (?, ?)", (trakt_id, time_in_seconds))
            cursor.connection.commit()
            cursor.close()
        except:
            import traceback
            traceback.print_exc()
        finally:
            control.try_release_lock(control.traktSyncDB_lock)
            try:
                cursor.close()
            except:
                pass

    def remove_bookmark(self, trakt_id):
        control.traktSyncDB_lock.acquire()
        try:
            cursor = self._get_cursor()
            cursor.execute("DELETE FROM bookmark WHERE trakt_id = ?", (trakt_id,))
            cursor.connection.commit()
            cursor.close()
        except:
            import traceback
            traceback.print_exc()
        finally:
            control.try_release_lock(control.traktSyncDB_lock)
            try:
                cursor.close()
            except:
                pass