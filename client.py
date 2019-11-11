from pymemcache.client.base import Client

def main():
    client = Client(('localhost', 11211))
    client.set('some_key', 'some_value')
    client.set('some_key1', 'some_value')
    client.set('some_key2', 'some_value')
    client.set('some_key3', 'some_value')
    client.set('some_key4', 'some_value')
    # client.set('some_key1', { "a": 3, "b": 1234, "c": 1234567 })
    # result = client.get('some_key')
    # client.set('some_key2', { "a": 3, "b": 1234, "c": 1234567 })
    # result = client.get('some_key')
    # client.set('some_key3', { "a": 3, "b": 1234, "c": 1234567 })
    # result = client.get('some_key')
    # print (result)
    result = client.get_multi(['some_key2', 'some_key3'])
    print (result)
    print (client.delete('some_key'))
    print (client.get('some_key'))
    client.set('new', 'unknown value')
    client.set('test1', 'tesing unknow reasonable text')
    client.set('test2', 'although i know it will be hash value')
    client.set('test3', 'show me the value')
    client.set('test4', 'whatever it takes')
    client.set('test5', 'something at works')
    return True

if __name__ == "__main__":
    main()