#!/usr/bin/env python
import asyncio
import sys
import os
import json
import sqlite3
from subprocess import Popen, call
from os import path
from database import Client, init_db

Database = None
def package(key, value, flags, exptime, bytes):
    '''
    VALUE <key> <flags> <bytes> [<cas unique>]\r\n
    <data block>\r\n
    '''
    value = decode(value)
    return f'VALUE {key} {flags} {bytes}\r\n{value}\r\n'
def encode(value):
    # value is always string but dict, array, etc.
    try:
        json_value = json.loads(value)
        value = json.dumps(json_value, ensure_ascii=False)
    except:
        pass
    return value
def decode(value):
    # value is always string but dict, array, etc.
    try:
        json_value = json.loads(value)
        value = json.dumps(json_value, ensure_ascii=False)
    except:
        pass
    return value
def get_value(key_list):
    select = []
    for key in key_list:
        try:
            row = Database.select(key)
        except sqlite3.Error as e:
            print ('sqlite error: ', e)
        if row is None:
            continue
        result = package(*row)
        select.append(result)
    result = ''.join(select) + 'END\r\n'
    return result.encode()

def set_value(key, value, flag, exptime, size):
    '''
    - "STORED\r\n", to indicate success.
    '''
    # print (key, value, flag, exptime, size)
    value = decode(value)
    try:
        Database.set(key, value, flag, size, exptime)
        return b'STORED\r\n'
    except sqlite3.Error as e:
        print ('sqlite error: ', e)
        return b'SERVER_ERROR\r\n'
def delete_value(key):
    '''
    delete <key> [noreply]\r\n
    response:
    - "DELETED\r\n" to indicate success
    - "NOT_FOUND\r\n" to indicate that the item with this key was not
        found.
    '''
    try:
        if Database.delete(key):
            return b'DELETED\r\n'
    except sqlite3.Error as e:
        print ('sqlite error: ', e)
    return b"NOT_FOUND\r\n"
def is_not_valid_input(key, flag, size, value):
    if ' ' in key:
        print ('space in key')
        return b'Key contains whitespace:'
    if isinstance(flag, int):
        print ('flag is not integer')
        return b'Flags is not an integer'
    if isinstance(size, int):
        return b'Length is not an integer'
    if int(size) != len(value):
        print (isinstance(len(value), int))
        print (size, len(value))
        return b'data block length mismatch'
    return False

async def handle_memcached_protocol(reader, writer):
    while True:
        try:
            data = await reader.readuntil(separator=b'\r\n')
        except asyncio.streams.IncompleteReadError:
            # print ('Incomplete error')
            break
        data = data.decode().replace('\r\n', '')
        cmd, *rest = data.split(' ')
        addr = writer.get_extra_info('peername')
        print(f"Received {data!r} from {addr!r}")
        if cmd == 'get':
            writer.write(get_value(rest))
        elif cmd == 'set':
            key, flag, exptime, size, *args = rest
            # size = int(size)
            # value = await reader.read(size)
            value = await reader.readuntil(separator=b'\r\n')
            value = value.decode().replace('\r\n', '')
            # if is_not_valid_input(key, flag, size, value):
            #     print ('not valid')
            #     '''
            #     - "CLIENT_ERROR <error>\r\n"
            #     means some sort of client error in the input line, i.e. the input
            #     doesn't conform to the protocol in some way. <error> is a
            #     human-readable error string.
            #     '''
            #     error_message = f'CLIENT_ERROR Key contains whitespace: \'{key}\''
            #     writer.write(error_message.encode())
            #     break
            result = set_value(key, value, flag, exptime, size)
            if len(args) == 0 or args[0] != 'noreply':
                writer.write(result)
        elif cmd == 'delete':
            result = delete_value(rest[0])
            if len(rest) == 1 or rest[1] != 'noreply':
                writer.write(result)
        else:
            writer.write(b'ERROR\r\n')
            '''
            - "ERROR\r\n"
            means the client sent a nonexistent command name.
            - "SERVER_ERROR <error>\r\n"
            means some sort of server error prevents the server from carrying
            out the command. <error> is a human-readable error string. In cases
            of severe server errors, which make it impossible to continue
            serving the client (this shouldn't normally happen), the server will
            close the connection after sending the error line. This is the only
            case in which the server closes a connection to a client.
            '''
        # else:
        #     break
        # print(f"Send: {message!r}")
        # writer.write(data)
    await writer.drain()
    print("connection closed")
    writer.close()

async def main(host, tcp_port):
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    # server = await loop.create_server(
    #     lambda: MemcachedServerProtocol(db_name),
    #     '127.0.0.1', 11211)
    server = await asyncio.start_server(
        handle_memcached_protocol, '127.0.0.1', 11211)
    
    addr = server.sockets[0].getsockname()
    # print(f'Serving on {addr} using MemcachedServerProtocol')
    print(f' * Serving on {addr} memcached Protocol')
    async with server:
        await server.serve_forever()
def start_react():
    pid = Popen(['npm', 'start'], cwd='./frontend').pid
    print (f"started react {pid}")
    return pid
def start_django(host, port):
    pid = Popen(["python", "manage.py", "runserver", f'{host}:{port}'], cwd="./http_server").pid
    return pid
def migrate_db():
    exitcode = call(["python", "manage.py", "makemigrations"], cwd="./http_server")
    print (f'completed makemigrations {exitcode}')
    exitcode = call(["python", "manage.py", "migrate"], cwd="./http_server")
    print (f'completed migration {exitcode}')
if __name__ == '__main__':
    if sys.argv[1] is None:
        print ('Please provide the sqlite db path')
        exit(1)
    # create sqlite
    db_file = path.abspath(sys.argv[1])
    # # start react server
    # react_pid = start_react()
    os.putenv('database', db_file)
    migrate_db()
    http_pid = start_django('127.0.0.1', 8080)
    print (f'running django process {http_pid}')

    Database = Client(db_file)
    Database.connect()
    asyncio.run(main('127.0.0.1', 11211), debug=True)
