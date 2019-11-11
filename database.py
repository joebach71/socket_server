import sys
import sqlite3

class Client():
    def __init__(self, db_file):
        self.db_file = db_file
        self.connect()
    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
    def select(self, key):
        c = self.conn.cursor()
        c.execute(f'SELECT key, value, flags, exptime, size from monitor_storage \
            WHERE key = \'{key}\'')
        row = c.fetchone()
        if row is None:
            return
        return row
    def set(self, key, value, flag, size, exptime=None):
        if self.select(key) is None:
            return self.insert(key, value, flag, size, exptime)
        else:
            return self.update(key, value, flag, size, exptime)
    def insert(self, key, value, flag, size, exptime=None):
        # Insert a row of data
        c = self.conn.cursor()
        statement = f"INSERT INTO monitor_storage (key, value, flags, exptime, size) \
            VALUES ('{key}', '{value}', {flag}, {exptime}, {size})"
        c.execute(statement)
        self.conn.commit()
        return True
    def update(self, key, value, flag, size, exptime=None):
        c = self.conn.cursor()
        c.execute(f"UPDATE monitor_storage SET \
            key='{key}', value='{value}', flags={flag}, exptime={exptime}, size={size} \
            WHERE key = '{key}'")
        print (key, value, flag, size, exptime)
        self.conn.commit()
    def delete(self, key):
        try:
            c = self.conn.cursor()
            c.execute(f'DELETE FROM monitor_storage WHERE key = \'{key}\'')
            self.conn.commit()
        except sqlite3.Error as err:
            print (err)
            return False
        return True
    def close(self):
        self.conn.close()
if __name__ == '__main__':
    init_db(sys.argv[0])
