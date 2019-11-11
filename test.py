import unittest
from unittest import mock
from database import Client as Sqlite3
import asyncio
from main import set_value, get_value, delete_value, handle_memcached_protocol
from pymemcache.client.base import Client
import sqlite3

def init_db(conn):
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    c = conn.cursor()
    # Create table
    c.execute('''CREATE TABLE monitor_storage
                (key text UNIQUE, value text, flags text, exptime integer, size integer)''')
    # Save (commit) the changes
    conn.commit()
    return conn

class TestDBTransactions(unittest.TestCase):
    def setUp(self):
        self.database = Sqlite3(':memory:')
        self.database.connect()
        init_db(self.database.conn)
    def tearDown(self):
        return super().tearDown()
        self.database.close()
    def test_insert(self):
        '''
        Test insert
        '''
        self.database.insert('foo', 'value', 1, 1, 10)
        self.assertEqual(self.database.select('foo'), ('foo', 'value', '1', 10, 1))
    def test_update(self):
        self.database.insert('foo', 'value', 1, 1, 11)
        self.database.update('foo', 'bar', 1, 1, 20)
        self.assertEqual(self.database.select('foo'), ('foo', 'bar', '1', 20, 1))
    def test_delete(self):
        self.database.insert('foo', 'bar', 1, 1, 20)
        self.assertEqual(self.database.select('foo'), ('foo', 'bar', '1', 20, 1))
        self.database.delete('foo')
        self.assertEqual(self.database.select('foo'), None)

# class TestMemcachedProtocol(unittest.TestCase):
#     '''
#     Test handle_memcached_protocol
#     '''
#     def _run(self, coro):
#         return asyncio.get_event_loop().run_until_complete(coro)
#     def setUp(self):
#         # set up sqlite3 db
#         self.database = Sqlite3(database=':memory:')
#         self.database.connect()
#         self.database.init_table()
#         self.loop = asyncio.get_event_loop()
#         self.f = asyncio.start_server(handle_memcached_protocol, \
#             '127.0.0.1', 11211, loop=self.loop)
#         # self.server = self.loop.run_until_complete(f)
#     def tearDown(self):
#         # # Serve requests until Ctrl+C is pressed
#         # print('Serving on {}'.format(server.sockets[0].getsockname()))
#         # try:
#         #     self.loop.run_forever()
#         # except KeyboardInterrupt:
#         #     pass

#         # Close the server
#         self.server.close()
#         self.loop.run_until_complete(self.server.wait_closed())
#         self.loop.close()
#         self.database.close()
#         return super().tearDown()
#     def test_get(self):
#         # Serve requests until Ctrl+C is pressed
#         self.assertRaises(ValueError, _run, \
#             handle_memcached_protocol)
#         print('Serving on {}'.format(self.server.sockets[0].getsockname()))
#         # try:
#         #     self.loop.run_forever()
#         # except KeyboardInterrupt:
#         #     pass
#         c = Client(('127.0.0.1', 11211))
#         c.set('integer', 1)
#         self.assertEqual(self.database.select('integer'), 1)
#     # def test_get_string(self):
#     #     self.database.insert('foo', 'bar', 1, 1, 'noreply')
#     #     self.assertEqual(self.database.select('foo'), 'bar')
#     # def test_get_list(self):
#     #     self.database.insert('list', ['a', 'b', 'c'], 1, 1, 'noreply')
#     #     self.assertEqual(self.database.select('foo'), 'bar')
#     # def test_set(self):
#     #     self.assertTrue('FOO'.isupper())
#     #     self.assertFalse('Foo'.isupper())
#     # def test_set_string(self):
#     #     pass
#     # def test_set_object(self):
#     #     pass
#     # def test_delete(self):
#     #     s = 'hello world'
#     #     self.assertEqual(s.split(), ['hello', 'world'])
#     #     # check that s.split fails when the separator is not a string
#     #     with self.assertRaises(TypeError):
#     #         s.split(2)
#     def test_bad_command(self):
#         pass

if __name__ == '__main__':
    unittest.main()