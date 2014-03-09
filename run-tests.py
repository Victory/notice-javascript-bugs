from subprocess import call

errs = 0
errs += call(["python", "tests/selenium/static-proxied.py"])
errs += call(["python", "tests/jasmine/jasmine-runner.py"])
exit(errs)
