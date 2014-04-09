import urllib2
import json


def qdb(db, method, data=''):
    db_url = 'http://127.0.0.1:5984/' + str(db)
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(db_url, data=data)
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: method
    try:
        data = opener.open(request).read()
    except urllib2.HTTPError, e:
        data = e.read()

    return json.loads(data)


def deletedb(name):
    dbs = qdb('_all_dbs', 'GET')
    if name in dbs:
        qdb(name, 'DELETE')


if __name__ == '__main__':
    dbname = 'injected'
    deletedb(dbname)
    qdb(dbname, 'PUT')
    result = qdb(dbname, 'POST', data='{"foo":3, "bar": "baz"}')
    doc_id = result['id']

    # little trick to query by id, by makin it like /dbname/doc_id
    from_db = qdb(dbname + "/" + doc_id, 'GET')
    assert from_db['foo'] == 3
    assert from_db['bar'] == "baz"
    deletedb(dbname)
