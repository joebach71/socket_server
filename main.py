#!/usr/bin/env python
import asyncio
import sys
from os import path

class MemcachedProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
    def eof_received(self):
        self.transport.close()
    def data_received(self, data):
        data = data.decode('utf-8').split(' ', 2)
        print (data)
        if data[0] == 'get':
            return self.get_value(data[1])
        elif data[0] == 'set':
            return self.set_value(data[1])
        elif data[0] == 'delete':
            return self.delete_value(data[1])
        else:
            self.transport.write('ERROR\r\n'.encode('utf-8'))
        # print('Close the client socket')
        # # self.transport.close()
    def get_value(self, key):
        print ('get method')
        self.transport.write(key.encode('utf-8'))
    def set_value(self, data):
        print ('set method')
        key, flag, exptime, noreply = data.split(' ')
        print (key, flag, exptime, noreply)
        self.transport.write(data.encode('utf-8'))
    def delete_value(self, key):
        print ('delete method')
        self.transport.write(key.encode('utf-8'))

async def main(host, tcp_port, http_port, database):
    '''TODO create sqlite '''
    '''TODO start http server '''
    loop = asyncio.get_running_loop()
    server = await loop.create_server(MemcachedProtocol, host, tcp_port)
    await server.serve_forever()
if __name__ == '__main__':
    if sys.argv[1] is None:
        print ('Please provide the sqlite db path')
        exit(1)
    asyncio.run(main('127.0.0.1', 11211, 8000, sys.argv[1]))
    