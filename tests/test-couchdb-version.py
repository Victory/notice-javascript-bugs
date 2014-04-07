import json
import unittest

import logging as log

from urllib2 import urlopen


class TestCouchDbVersion(unittest.TestCase):
    def test_coudb_listening(self):
        urlh = urlopen('http://127.0.0.1:5984/')
        json_data = urlh.read()
        couch_info = json.loads(json_data)

    def test_couchdb_version(self):
        urlh = urlopen('http://127.0.0.1:5984/')
        json_data = urlh.read()
        couch_info = json.loads(json_data)

        assert 'couchdb' in couch_info
        assert 'version' in couch_info
        assert couch_info['version'] == '1.0.1'


if __name__ == "__main__":
    log.info('Running Version Unit Tests')
    unittest.main()
