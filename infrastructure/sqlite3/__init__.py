import contextlib
import sqlite3


@contextlib.contextmanager
def get_conn():
    database = 'pca.db'
    conn = sqlite3.connect(database)
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()
