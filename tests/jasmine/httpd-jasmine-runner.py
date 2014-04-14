import sys
import os
from os.path import dirname, realpath
project_base = dirname(dirname(dirname(realpath(__file__))))
sys.path.append(project_base + "/external/mitm-http-proxy")

from time import sleep

from selenium import webdriver

from MitmHttpProxy import Httpd, shutdown_thread


import urllib2
import json


if __name__ == '__main__':
    sleep(2)
    os.chdir(dirname(realpath(__file__)) + "/lib")

    http_port = "8000"

    httpd = Httpd()
    httpd.start()

    driver = webdriver.Firefox()
    driver.get("http://127.0.0.1:" + http_port + "/SpecCouchdb.html")
    sleep(2)
    driver.close()

    shutdown_thread(httpd)
