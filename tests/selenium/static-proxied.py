import tempfile
from os.path import dirname, realpath
from os import remove

from selenium import webdriver

print "Running Static Proxied Tests"

BASEDIR = dirname(dirname(dirname(realpath(__file__))))
REAL_FILE_PATH = BASEDIR + "/src/static-proxied.html"

tmpfile = tempfile.NamedTemporaryFile(delete=False)

real_file = open(REAL_FILE_PATH, 'r').read()

# some versions of firefox don't call window.onerror for manual throws
# so this may not work
injection = """
<script>
  window.addEventListener('error', function(err) {
    var body = document.getElementsByTagName('body')[0];
    var wasError = document.createElement('p');
    wasError.setAttribute('id','injectedErrorTest');
    var text = document.createTextNode('INJECTED-ERROR-TEST');
    wasError.appendChild(text);
    body.appendChild(wasError);
  });
</script>
"""

injected_file = real_file.replace('<head>', '<head>' + injection)
tmpfile.write(injected_file)
tmpfile.close()


fake_home = "file://" + tmpfile.name
driver = webdriver.Firefox()

driver.get(fake_home)
remove(tmpfile.name)

injectedErrorTest = driver.find_element_by_id('injectedErrorTest')
assert injectedErrorTest
assert injectedErrorTest.text == 'INJECTED-ERROR-TEST'

driver.close()
