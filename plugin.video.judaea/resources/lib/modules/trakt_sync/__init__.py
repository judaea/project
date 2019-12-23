# -*- coding: utf-8 -*-

from datetime import datetime

from resources.lib.modules import control
from resources.lib.modules.worker import ThreadPool

try:
    from Queue import Queue
except:
    from queue import Queue

try:
    from sqlite3 import dbapi2 as db, OperationalError
except ImportError:
    from pysqlite2 import dbapi2 as db, OperationalError

database_path = control.traktSyncDB


class TraktSyncDatabase:
    def __init__(self):

        self.activites = {}

        self._build_show_table()
        self._build_episode_table()
        self._build_movies_table()
        self._build_hidden_items()
        self._build_sync_activities()
        self._build_season_table()
        self._build_bookmark_table()
        self._build_lists_table()

        self.item_list = []
        self.threads = []
        self.task_queue = ThreadPool(workers=4)
        self.queue_finished = False
        self.task_len = 0
        self.base_date = '1970-01-01T00:00:00'
        self.number_of_threads = 20

        # If you make changes to the required meta in any indexer that is cached in this database
        # You will need to update the below version number to match the new addon version
        # This will ensure that the metadata required for operations is available
        # You may also update this version number to force a rebuild of the database after updating Judaea
        self.last_meta_update = '1.6.1'

        control.traktSyncDB_lock.acquire()

        self._refresh_activites()

        if self.activites is None:
            cursor = self._get_cursor()
            meta = '{}'
            cursor.execute("UPDATE shows SET kodi_meta=?", (meta,))
            cursor.execute("UPDATE seasons SET kodi_meta=?", (meta,))
            cursor.execute("UPDATE episodes SET kodi_meta=?", (meta,))
            cursor.execute("UPDATE movies SET kodi_meta=?", (meta,))
            cursor.connection.commit()

            self._set_base_activites()

            cursor.execute('SELECT * FROM activities WHERE sync_id=1')
            self.activites = cursor.fetchone()
            cursor.close()

        control.try_release_lock(control.traktSyncDB_lock)

        if self.activites is not None:
            self._check_database_version()

    def _refresh_activites(self):
        cursor = self._get_cursor()
        cursor.execute('SELECT * FROM activities WHERE sync_id=1')
        self.activites = cursor.fetchone()
        cursor.close()

    def _set_base_activites(self):
        cursor = self._get_cursor()
        cursor.execute('INSERT INTO activities(sync_id, all_activities, shows_watched, movies_watched,'
                       ' movies_collected, shows_collected, hidden_sync, shows_meta_update, movies_meta_update,'
                       'judaea_version, trakt_username, movies_bookmarked, episodes_bookmarked, lists_sync) '
                       'VALUES(1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (self.base_date, self.base_date, self.base_date, self.base_date, self.base_date,
                        self.base_date, self.base_date, self.base_date, self.last_meta_update,
                        control.getSetting('trakt.username'), self.base_date, self.base_date, self.base_date))

        cursor.connection.commit()
        self.activites = cursor.fetchone()
        cursor.close()



    def _check_database_version(self):
        # If we are updating from a database prior to database versioning, we must clear the meta data
        # Migrate from older versions before trakt username tracking
        if 'trakt_username' not in self.activites and control.getSetting('trakt.auth') != '':
            control.traktSyncDB_lock.acquire()
            control.log('Upgrading Trakt Sync Database Version to support Trakt username identification')
            cursor = self._get_cursor()
            cursor.execute('ALTER TABLE activities ADD COLUMN trakt_username TEXT')
            cursor.execute('UPDATE activities SET trakt_username = ?', (control.getSetting('trakt.username'),))
            cursor.connection.commit()
            cursor.close()
            control.try_release_lock(control.traktSyncDB_lock)

        # Migrate from an old version before database migrations
        if 'judaea_version' not in self.activites:
            control.log('Upgrading Trakt Sync Database Version')
            self.clear_all_meta(False)
            control.traktSyncDB_lock.acquire()
            cursor = self._get_cursor()
            cursor.execute('ALTER TABLE activities ADD COLUMN judaea_version TEXT')
            cursor.execute('UPDATE activities SET judaea_version = ?', (self.last_meta_update,))
            cursor.connection.commit()
            cursor.close()
            control.try_release_lock(control.traktSyncDB_lock)

        if control.check_version_numbers(self.activites['judaea_version'], self.last_meta_update):
            control.log('Rebuilding Trakt Sync Database Version')
            self.re_build_database(True)
            return

        if 'movies_bookmarked' not in self.activites:
            control.log('Upgrading Trakt Sync Database Version to support bookmark sync')
            control.traktSyncDB_lock.acquire()
            cursor = self._get_cursor()
            cursor.execute('ALTER TABLE activities ADD COLUMN movies_bookmarked TEXT')
            cursor.execute('ALTER TABLE activities ADD COLUMN episodes_bookmarked TEXT')
            cursor.connection.commit()
            cursor.execute('UPDATE activities SET movies_bookmarked = ?', (self.base_date,))
            cursor.execute('UPDATE activities SET episodes_bookmarked = ?', (self.base_date,))
            cursor.connection.commit()
            cursor.close()
            control.try_release_lock(control.traktSyncDB_lock)

        control.traktSyncDB_lock.acquire()
        cursor = self._get_cursor()
        cursor.execute('SELECT 1 FROM sqlite_master WHERE type = \'table\' AND name = \'shows\' AND sql LIKE '
                       '\'%air_date%\'')
        if len(cursor.fetchall()) == 0:
            cursor.execute('ALTER TABLE shows ADD COLUMN air_date DATE')
            cursor.connection.commit()
        cursor.execute('SELECT 1 FROM sqlite_master WHERE type = \'table\' AND name = \'episodes\' AND sql LIKE '
                       '\'%air_date%\'')
        if len(cursor.fetchall()) == 0:
            cursor.execute('ALTER TABLE episodes ADD COLUMN air_date DATE')
            cursor.connection.commit()
        cursor.execute('SELECT 1 FROM sqlite_master WHERE type = \'table\' AND name = \'seasons\' AND sql LIKE '
                       '\'%air_date%\'')
        if len(cursor.fetchall()) == 0:
            cursor.execute('ALTER TABLE seasons ADD COLUMN air_date DATE')
            cursor.connection.commit()
        cursor.execute('SELECT 1 FROM sqlite_master WHERE type = \'table\' AND name = \'movies\' AND sql LIKE '
                       '\'%air_date%\'')
        if len(cursor.fetchall()) == 0:
            cursor.execute('ALTER TABLE movies ADD COLUMN air_date DATE')
            cursor.connection.commit()
        cursor.execute('SELECT 1 FROM sqlite_master WHERE type = \'table\' AND name = \'lists\' AND sql LIKE '
                       '\'%slug TEXT NOT NULL)\'')
        if len(cursor.fetchall()) > 0:
            cursor.execute('ALTER TABLE lists RENAME TO lists_old')
            cursor.execute('CREATE TABLE IF NOT EXISTS lists ('
                           'trakt_id INTEGER NOT NULL, '
                           'media_type TEXT NOT NULL,'
                           'name TEXT NOT NULL, '
                           'username TEXT NOT NULL, '
                           'kodi_meta TEXT NOT NULL, '
                           'updated_at TEXT NOT NULL,'
                           'list_type TEXT NOT NULL,'
                           'item_count INT NOT NULL,'
                           'sort_by TEXT NOT NULL,'
                           'sort_how TEXT NOT NULL,'
                           'slug TEXT NOT NULL,'
                           'PRIMARY KEY (trakt_id, media_type)) '
                           )
            cursor.execute('insert into lists select * from lists_old')
            cursor.execute('DROP TABLE IF EXISTS lists_old')
            cursor.connection.commit()
        control.try_release_lock(control.traktSyncDB_lock)

        if 'movies_bookmarked' not in self.activites:
            control.log('Upgrading Trakt Sync Database Version to support bookmark sync')
            cursor = self._get_cursor()
            cursor.execute('ALTER TABLE activities ADD COLUMN movies_bookmarked TEXT')
            cursor.execute('ALTER TABLE activities ADD COLUMN episodes_bookmarked TEXT')
            cursor.connection.commit()
            cursor.execute('UPDATE activities SET movies_bookmarked = ?', (self.base_date,))
            cursor.execute('UPDATE activities SET episodes_bookmarked = ?', (self.base_date,))
            cursor.connection.commit()
            cursor.close()

    def _build_show_table(self):
        control.traktSyncDB_lock.acquire()
        cursor = self._get_cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS shows '
                       '(trakt_id INTEGER PRIMARY KEY, '
                       'kodi_meta TEXT NOT NULL, '
                       'last_updated TEXT NOT NULL, '
                       'air_date TEXT, '
                       'UNIQUE(trakt_id))')
        cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS ix_shows ON "shows" (trakt_id ASC )')
        cursor.connection.commit()
        cursor.close()
        control.try_release_lock(control.traktSyncDB_lock)

    def _build_episode_table(self):
        control.traktSyncDB_lock.acquire()
        cursor = self._get_cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS episodes ('
                       'show_id INTEGER NOT NULL, '
                       'trakt_id INTEGER NOT NULL PRIMARY KEY, '
                       'season INTEGER NOT NULL, '
                       'kodi_meta TEXT NOT NULL, '
                       'last_updated TEXT NOT NULL, '
                       'watched INTEGER NOT NULL, '
                       'collected INTEGER NOT NULL, '
                       'number INTEGER NOT NULL, '
                       'air_date TEXT, '
                       'UNIQUE (trakt_id),'
                       'FOREIGN KEY(show_id) REFERENCES shows(trakt_id) ON DELETE CASCADE)')
        cursor.execute(
            'CREATE UNIQUE INDEX IF NOT EXISTS ix_episodes ON episodes (show_id ASC, season ASC, number ASC)')
        cursor.connection.commit()
        cursor.close()
        control.try_release_lock(control.traktSyncDB_lock)

    def _build_season_table(self):
        control.traktSyncDB_lock.acquire()
        cursor = self._get_cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS seasons ('
                       'show_id INTEGER NOT NULL, '
                       'season INTEGER NOT NULL, '
                       'kodi_meta TEXT NOT NULL, '
                       'air_date TEXT, '
                       'FOREIGN KEY(show_id) REFERENCES shows(trakt_id) ON DELETE CASCADE)')
        cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS ix_season ON seasons (show_id ASC, season ASC)')
        cursor.connection.commit()
        cursor.close()
        control.try_release_lock(control.traktSyncDB_lock)

    def _build_movies_table(self):
        control.traktSyncDB_lock.acquire()
        cursor = self._get_cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS movies ('
                       'trakt_id INTEGER NOT NULL PRIMARY KEY, '
                       'kodi_meta TEXT NOT NULL, '
                       'collected INTEGER NOT NULL, '
                       'watched INTEGER NOT NULL, '
                       'last_updated INTEGER NOT NULL, '
                       'air_date TEXT, '
                       'UNIQUE (trakt_id))')
        cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS ix_movies ON movies (trakt_id ASC)')
        cursor.connection.commit()
        cursor.close()
        control.try_release_lock(control.traktSyncDB_lock)

    def _build_hidden_items(self):
        control.traktSyncDB_lock.acquire()
        cursor = self._get_cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS hidden ('
                       'id_section TEXT NOT NULL, '
                       'trakt_id INTEGER NOT NULL, '
                       'item_type TEXT NOT NULL, '
                       'section TEXT NOT NULL, '
                       'UNIQUE (id_section))')

        cursor.connection.commit()
        cursor.close()
        control.try_release_lock(control.traktSyncDB_lock)

    def _build_sync_activities(self):
        control.traktSyncDB_lock.acquire()
        cursor = self._get_cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS activities ('
                       'sync_id INTEGER PRIMARY KEY, '
                       'all_activities TEXT NOT NULL, '
                       'shows_watched TEXT NOT NULL, '
                       'movies_watched TEXT NOT NULL, '
                       'shows_collected TEXT NOT NULL, '
                       'movies_collected TEXT NOT NULL, '
                       'hidden_sync TEXT NOT NULL,'
                       'shows_meta_update TEXT NOT NULL,'
                       'movies_meta_update TEXT NOT NULL,'
                       'judaea_version TEXT NOT NULL,'
                       'trakt_username TEXT,'
                       'movies_bookmarked TEXT NOT NULL,'
                       'episodes_bookmarked TEXT NOT NULL,'
                       'lists_sync TEXT NOT NULL) '
                       )
        cursor.connection.commit()
        cursor.close()
        control.try_release_lock(control.traktSyncDB_lock)

    def _build_lists_table(self):
        control.traktSyncDB_lock.acquire()
        cursor = self._get_cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS lists ('
                       'trakt_id INTEGER NOT NULL, '
                       'media_type TEXT NOT NULL,'
                       'name TEXT NOT NULL, '
                       'username TEXT NOT NULL, '
                       'kodi_meta TEXT NOT NULL, '
                       'updated_at TEXT NOT NULL,'
                       'list_type TEXT NOT NULL,'
                       'item_count INT NOT NULL,'
                       'sort_by TEXT NOT NULL,'
                       'sort_how TEXT NOT NULL,'
                       'slug TEXT NOT NULL,'
                       'PRIMARY KEY (trakt_id, media_type)) '
                       )

        cursor.connection.commit()
        cursor.close()
        control.try_release_lock(control.traktSyncDB_lock)

    def _build_bookmark_table(self):
        control.traktSyncDB_lock.acquire()
        cursor = self._get_cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS bookmark (trakt_id TEXT, timeInSeconds TEXT, UNIQUE(trakt_id))")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_bookmark ON bookmark (trakt_id)")
        cursor.close()
        control.try_release_lock(control.traktSyncDB_lock)

    def _build_bookmark_table(self):
        cursor = self._get_cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS bookmark (trakt_id TEXT, timeInSeconds TEXT, UNIQUE(trakt_id))")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_bookmark ON bookmark (trakt_id)")
        cursor.close()

    def _get_cursor(self):
        conn = _get_connection()
        conn.execute("PRAGMA FOREIGN_KEYS = 1")
        cursor = conn.cursor()
        return cursor

    def flush_activities(self, clear_meta=False):
        if clear_meta:
            self.clear_all_meta()
        control.traktSyncDB_lock.acquire()
        cursor = self._get_cursor()
        cursor.execute('DROP TABLE activities')
        cursor.connection.commit()
        cursor.close()
        control.try_release_lock(control.traktSyncDB_lock)

    def clear_user_information(self):
        control.traktSyncDB_lock.acquire()
        cursor = self._get_cursor()
        cursor.execute('UPDATE episodes SET watched=0')
        cursor.execute('UPDATE episodes SET collected=0')
        cursor.execute('UPDATE movies SET watched=0')
        cursor.execute('UPDATE movies SET collected=0')
        cursor.connection.commit()
        cursor.close()
        control.try_release_lock(control.traktSyncDB_lock)
        self.set_trakt_user('')
        control.showDialog.notification(control.addonName + ': Trakt', control.lang(40260), time=5000)

    def set_trakt_user(self, trakt_username):
        control.traktSyncDB_lock.acquire()
        cursor = self._get_cursor()
        control.log('Setting Trakt Username: %s' % trakt_username)
        cursor.execute('UPDATE activities SET trakt_username=?', (trakt_username,))
        cursor.connection.commit()
        cursor.close()
        control.try_release_lock(control.traktSyncDB_lock)

    def clear_all_meta(self, notify=True):
        if notify:
            confirm = control.showDialog.yesno(control.addonName, control.lang(40139))
            if confirm == 0:
                return
        control.traktSyncDB_lock.acquire()
        meta = '{}'
        cursor = self._get_cursor()
        cursor.execute("UPDATE shows SET kodi_meta=?", (meta,))
        cursor.execute("UPDATE seasons SET kodi_meta=?", (meta,))
        cursor.execute("UPDATE episodes SET kodi_meta=?", (meta,))
        cursor.execute("UPDATE movies SET kodi_meta=?", (meta,))
        cursor.connection.commit()
        cursor.close()
        control.try_release_lock(control.traktSyncDB_lock)
        control.showDialog.notification(control.addonName + ': Trakt', control.lang(40261), time=5000)

    def clear_specific_meta(self, trakt_object):
        if 'seasons' in trakt_object:
            show_id = trakt_object['show_id']
            season_no = trakt_object['seasons'][0]['number']
            control.traktSyncDB_lock.acquire()
            cursor = self._get_cursor()
            cursor.execute('UPDATE episodes SET kodi_meta=? WHERE show_id=? AND season=?', ('{}', show_id, season_no))
            cursor.execute('UPDATE seasons SET kodi_meta=? WHERE show_id=? AND season=?', ('{}', show_id, season_no))
            cursor.connection.commit()
            cursor.close()
            control.try_release_lock(control.traktSyncDB_lock)

        elif 'shows' in trakt_object:
            show_id = trakt_object['shows'][0]['ids']['trakt']
            control.traktSyncDB_lock.acquire()
            cursor = self._get_cursor()
            cursor.execute('UPDATE shows SET kodi_meta=? WHERE trakt_id=?', ('{}', show_id))
            cursor.execute('UPDATE episodes SET kodi_meta=? WHERE show_id=? ', ('{}', show_id))
            cursor.execute('UPDATE seasons SET kodi_meta=? WHERE show_id=? ', ('{}', show_id))
            cursor.connection.commit()
            cursor.close()
            control.try_release_lock(control.traktSyncDB_lock)

        elif 'episodes' in trakt_object:
            trakt_id = trakt_object['episodes'][0]['ids']['trakt']
            control.traktSyncDB_lock.acquire()
            cursor = self._get_cursor()
            cursor.execute('UPDATE episodes SET kodi_meta=? WHERE trakt_id=? ', ('{}', trakt_id))
            cursor.connection.commit()
            cursor.close()
            control.try_release_lock(control.traktSyncDB_lock)

        elif 'movies' in trakt_object:
            trakt_id = trakt_object['movies'][0]['ids']['trakt']
            control.traktSyncDB_lock.acquire()
            cursor = self._get_cursor()
            cursor.execute('UPDATE movies SET kodi_meta=? WHERE trakt_id=? ', ('{}', trakt_id))
            cursor.connection.commit()
            cursor.close()
            control.try_release_lock(control.traktSyncDB_lock)

    def re_build_database(self, silent=False):
        if not silent:
            confirm = control.showDialog.yesno(control.addonName, control.lang(40139))
            if confirm == 0:
                return

        control.traktSyncDB_lock.acquire()
        cursor = self._get_cursor()
        cursor.execute('DROP TABLE IF EXISTS shows')
        cursor.execute('DROP TABLE IF EXISTS seasons')
        cursor.execute('DROP TABLE IF EXISTS episodes')
        cursor.execute('DROP TABLE IF EXISTS movies')
        cursor.execute('DROP TABLE IF EXISTS activities')
        cursor.execute('DROP TABLE IF EXISTS hidden')
        cursor.execute('DROP TABLE IF EXISTS lists')
        cursor.execute('DROP TABLE IF EXISTS bookmark')
        cursor.connection.commit()
        cursor.close()
        control.try_release_lock(control.traktSyncDB_lock)

        self._build_show_table()
        self._build_episode_table()
        self._build_movies_table()
        self._build_hidden_items()
        self._build_sync_activities()
        self._build_season_table()
        self._build_lists_table()
        self._build_bookmark_table()

        self._set_base_activites()
        self._refresh_activites()

        from resources.lib.modules.trakt_sync import activities
        sync_errors = activities.TraktSyncDatabase().sync_activities(silent)

        if sync_errors:
            control.showDialog.notification(control.addonName + ': Trakt', control.lang(40353), time=5000)
        elif sync_errors is None:
            self._refresh_activites()
            return
        else:
            control.showDialog.notification(control.addonName + ': Trakt', control.lang(40262), time=5000)


def _bring_out_your_dead(population):
    dead = None
    remaining_population = [i for i in population if i is not dead]
    return remaining_population


def _utc_now_as_trakt_string():
    date = datetime.utcnow()
    return date.strftime(control.trakt_gmt_format)


def _strf_local_date(datetime_object):
    return datetime_object.strftime('%Y-%m-%dT%H:%M:%S')


def _parse_local_date_format(datestring):
    return control.datetime_workaround(datestring, control.trakt_gmt_format.strip('.000Z'), date_only=False)


def _requires_update(new_date, old_date):
    if control.datetime_workaround(new_date, control.trakt_gmt_format, False) > \
            control.datetime_workaround(old_date, '%Y-%m-%dT%H:%M:%S', False):
        return True
    else:
        return False


def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def _get_connection():
    control.makeFile(control.dataPath)
    conn = db.connect(database_path, timeout=60.0)
    conn.row_factory = _dict_factory
    return conn
