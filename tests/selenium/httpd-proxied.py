import sys
import os
from os.path import dirname, realpath
project_base = dirname(dirname(dirname(realpath(__file__))))
sys.path.append(project_base + "/external/mitm-http-proxy")

from time import sleep

from selenium import webdriver

from MitmHttpProxy import MitmHttpProxy, Httpd, shutdown_thread

if __name__ == '__main__':
    os.chdir(project_base + "/src")

    onerror = """
<script>
// couchdb query will happen here
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

    driver = webdriver.Firefox()
    driver.get("http://127.0.0.1:" + inport + "/httpd-proxied.html")
    sleep(1)
    driver.close()

    shutdown_thread(cap)
    shutdown_thread(httpd)
