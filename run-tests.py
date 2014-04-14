from subprocess import call

errs = 0
errs += call(["python", "tests/test-couchdb-version.py"])
errs += call(["python", "tests/test-create-couchdb-and-insert.py"])
errs += call(["python", "tests/selenium/static-proxied.py"])
errs += call(["python", "tests/jasmine/jasmine-runner.py"])
errs += call(["python", "tests/selenium/httpd-proxied.py"])
errs += call(["python", "tests/jasmine/httpd-jasmine-runner.py"])
exit(errs)
