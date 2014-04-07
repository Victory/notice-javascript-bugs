import sys
import os
from os.path import dirname, realpath
project_base = dirname(dirname(dirname(realpath(__file__))))
sys.path.append(project_base + "/external/mitm-http-proxy")

from MitmHttpProxy import MitmHttpProxy, Httpd, shutdown_thread

if __name__ == '__main__':
    os.chdir(project_base + "/src")

    inport = "8777"
    http_port = "8000"

    httpd = Httpd()
    httpd.start()

    cap = MitmHttpProxy(
        '127.0.0.1', int(inport),
        '127.0.0.1', int(http_port))

    shutdown_thread(cap)
    shutdown_thread(httpd)
