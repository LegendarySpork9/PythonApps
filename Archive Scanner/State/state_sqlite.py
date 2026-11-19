import logging
import os
import sqlite3
import time

from State import StateBackend

logger = logging.getLogger("archive_scanner.state_sqlite")

RETRY_DELAY_SECONDS = 5

SCHEMA_SQL = """\
CREATE TABLE IF NOT EXISTS SeenWorks (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    ScannerTag TEXT NOT NULL,
    WorkId INTEGER NOT NULL,
    DateAdded TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(ScannerTag, WorkId)
);

CREATE INDEX IF NOT EXISTS IX_SeenWorks_ScannerTag
    ON SeenWorks(ScannerTag);
"""


class SqliteStateBackend(StateBackend):
    def __init__(self, db_path: str):
        self._db_path = db_path
        self._ensure_schema()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, timeout=10)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _ensure_schema(self) -> None:
        db_dir = os.path.dirname(self._db_path)

        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

        conn = self._execute_with_retry(self._get_connection)

        try:
            conn.executescript(SCHEMA_SQL)
            conn.commit()
        finally:
            conn.close()

    def _execute_with_retry(self, operation, *args):
        try:
            return operation(*args)
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                logger.warning(
                    "Database locked, retrying in %d seconds", RETRY_DELAY_SECONDS
                )
                time.sleep(RETRY_DELAY_SECONDS)
                return operation(*args)
            raise

    def load(self, key: str) -> list[int]:
        def _query():
            conn = self._get_connection()
            try:
                cursor = conn.execute(
                    "SELECT WorkId FROM SeenWorks WHERE ScannerTag = ? ORDER BY Id",
                    (key,),
                )
                return [row[0] for row in cursor.fetchall()]
            finally:
                conn.close()

        return self._execute_with_retry(_query)

    def save(self, key: str, work_ids: list[int]) -> None:
        def _write():
            conn = self._get_connection()
            try:
                conn.execute("DELETE FROM SeenWorks WHERE ScannerTag = ?", (key,))
                conn.executemany(
                    "INSERT INTO SeenWorks (ScannerTag, WorkId) VALUES (?, ?)",
                    [(key, wid) for wid in work_ids],
                )
                conn.commit()
            finally:
                conn.close()

        self._execute_with_retry(_write)

    def add_works(self, key: str, new_ids: list[int]) -> None:
        def _insert():
            conn = self._get_connection()
            try:
                conn.executemany(
                    "INSERT OR IGNORE INTO SeenWorks (ScannerTag, WorkId) VALUES (?, ?)",
                    [(key, wid) for wid in new_ids],
                )
                conn.commit()
            finally:
                conn.close()

        self._execute_with_retry(_insert)

    def get_all_keys(self) -> list[str]:
        def _query():
            conn = self._get_connection()
            try:
                cursor = conn.execute(
                    "SELECT DISTINCT ScannerTag FROM SeenWorks ORDER BY ScannerTag"
                )
                return [row[0] for row in cursor.fetchall()]
            finally:
                conn.close()

        return self._execute_with_retry(_query)
