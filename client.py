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
    return True

if __name__ == "__main__":
    main()