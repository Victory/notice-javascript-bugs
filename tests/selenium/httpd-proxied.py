import sys
import os
from os.path import dirname, realpath
project_base = dirname(dirname(dirname(realpath(__file__))))
sys.path.append(project_base + "/external/mitm-http-proxy")

import urllib2
import json

from time import sleep

from selenium import webdriver

from MitmHttpProxy import MitmHttpProxy, Httpd, shutdown_thread


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


if __name__ == '__main__':

    chromedriver = os.getcwd() + "/chromedriver"
    print chromedriver
    os.environ["webdriver.chrome.driver"] = chromedriver

    print "Running: Real injection over httpd, with selenium and couchdb"
    os.chdir(project_base + "/src")

    onerror = """
<script>
var corsIsDoneFlag = false;
var corsResult = false;
function corsIsDone() {
  corsIsDoneFlag = true;
}
// Create the XHR object.
function createCORSRequest(method, url) {
  var xhr = new XMLHttpRequest();
  if ("withCredentials" in xhr) {
    // XHR for Chrome/Firefox/Opera/Safari.
    xhr.open(method, url, true);
  } else if (typeof XDomainRequest != "undefined") {
    // XDomainRequest for IE.
    xhr = new XDomainRequest();
    xhr.open(method, url);
  } else {
    // CORS not supported.
    xhr = null;
  }
  xhr.setRequestHeader("Content-Type","application/json");
  return xhr;
}
function makeCorsRequest(uri, method, data, done) {
  console.log("got uri: " + uri);
  var xhr = createCORSRequest(method, uri);
  if (!xhr) {
    console.log('CORS not supported');
    done();
    return;
  }
  // Response handlers.
  xhr.onload = function() {
    console.log('OK:' + xhr.responseText);
    corsResult = xhr.responseText;
    done();
  };
  xhr.onerror = function() {
    console.log('ERROR: ' + uri + '.');
    done();
  };
  xhr.send(data);
}

var errHandler = function (evt, url, lineNumber) {
  var baseUrl = 'http://127.0.0.1:5984';
  var path = '/injected';
  var url = baseUrl + path;


  var error = {}
  error = {
     'foundError': true,
     'filename': evt.filename || document.location.href,
     'lineno': evt.lineno || lineNumber || -1,
     'type': evt.type || 'unknown type',
     'message': evt.message || evt,
     'userAgent': navigator.userAgent || 'unknown ua'
  };
  console.log(error);
  var data = JSON.stringify(error);
  var method = 'POST';
  makeCorsRequest(url, method, data, corsIsDone);
  return true;
};
window.onerror = errHandler;
</script>
"""
    inport = "8777"
    http_port = "8000"

    httpd = Httpd()
    httpd.start()

    cap = MitmHttpProxy(
        '127.0.0.1', int(inport),
        '127.0.0.1', int(http_port))
    cap.start()
    cap.join(2)

    def ijb(body):
        body = body.replace(
            "<head>",
            "<head>" + onerror)
        return body

    cap.inject_body_function = ijb

    # conditionally delete then create a new "injected" db
    dbname = 'injected'
    dbs = qdb('_all_dbs', 'GET')
    if dbname in dbs:
        qdb(dbname, 'DELETE')
    qdb(dbname, 'PUT')

    driver = webdriver.Chrome(chromedriver)
    driver.get("http://127.0.0.1:" + inport + "/httpd-proxied.html")
    sleep(1)
    driver.close()

    shutdown_thread(cap)
    shutdown_thread(httpd)

    allRecords = qdb(dbname + "/_all_docs", 'GET')

    doc_id = allRecords['rows'][0]['key']
    from_db = qdb(dbname + "/" + doc_id, 'GET')

    keys = ['foundError', 'filename', 'lineno',
            'type', 'message', 'userAgent']

    for key in keys:
        assert key in from_db
        print key, ':', from_db[key]
