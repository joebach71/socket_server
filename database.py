import sys
import sqlite3

def init_db(database):
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    print (database)
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # Create table
    c.execute('''CREATE TABLE memcached
                (key text UNIQUE, value text, flag integer, exptime integer, size integer)''')
    # Save (commit) the changes
    conn.commit()
    return conn

class Client():
    def __init__(self, db_file):
        self.db_file = db_file
        self.connect()
    def init_table(self):
        c = self.conn.cursor()
        # Create table
        c.execute(f'CREATE TABLE memcached \
                    (key text UNIQUE, value text, flag integer, exptime integer, size integer)')
        # Save (commit) the changes
        self.conn.commit()
    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
    def select(self, key):
        c = self.conn.cursor()
        c.execute(f'SELECT * from memcached WHERE key = \'{key}\'')
        row = c.fetchall()
        print (row)
        if len(row) == 1:
            return row[0]
    def set(self, key, value, flag, size, exptime=None):
        if self.select(key) is None:
            self.insert(key, value, flag, size, exptime)
        else:
            self.update(key, value, flag, size, exptime)
    def insert(self, key, value, flag, size, exptime=None):
        # Insert a row of data
        try:
            c = self.conn.cursor()
            statement = f"INSERT INTO memcached VALUES \
                ('{key}','{value}', {flag}, {exptime}, {size})"
            c.execute(statement)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print ('caught error on insert', e)
        return False
    def update(self, key, value, flag, size, exptime=None):
        c = self.conn.cursor()
        c.execute(f"UPDATE memcached SET \
            key='{key}', value='{value}', flag={flag}, exptime={exptime}, size={size} \
            WHERE key = '{key}'")
        print (key, value, flag, size, exptime)
        self.conn.commit()
        print ('update completed')
    def delete(self, key):
        try:
            c = self.conn.cursor()
            c.execute(f'DELETE FROM memcached WHERE key = \'{key}\'')
            self.conn.commit()
        except sqlite3.Error as err:
            print (err)
            return False
        return True
    def close(self):
        self.conn.close()
if __name__ == '__main__':
    init_db(sys.argv[0])
