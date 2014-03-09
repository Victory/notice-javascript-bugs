import sys
import cStringIO
import contextlib
from os.path import dirname, realpath

from selenium import webdriver

BASEDIR = dirname(realpath(__file__))
HOME = "file://" + BASEDIR + "/lib"


@contextlib.contextmanager
def silence():
    real_stdout = sys.stdout
    sys.stdout = cStringIO.StringIO()
    yield
    sys.stdout = real_stdout


def run_jasmine(driver, spec_htmls):

    fail_count = 0
    for spec_html in spec_htmls:
        print "Running", spec_html

        driver.get(HOME + "/" + spec_html)

        bars = driver.find_elements_by_css_selector('.bar')
        for bar in bars:
            if 'failed' in bar.get_attribute('class'):
                print "**" + bar.text + "**"

        results = driver.find_element_by_css_selector('.results')
        failures = results.find_element_by_css_selector('.failures')
        details = failures.find_elements_by_css_selector('.failed')

        for detail in details:
            desc = detail.find_element_by_css_selector('.description')
            message = detail.find_element_by_css_selector('.result-message')
            print desc.text
            print " -", message.text
            fail_count += 1

    return fail_count

if __name__ == '__main__':
    print "Running jasmine..."

    spec_htmls = ['SpecPass.html',
                 'SpecRunner.html']

    driver = webdriver.Firefox()

    # test that failures are still showing up

    with silence():
        fail_count = run_jasmine(driver, ['SpecFail.html'])
    if fail_count == 0:
        print "Jasmine Tests are Not Operational"
        run_jasmine(driver, ['SpecFail.html'])
        exit(1)

    fail_count = run_jasmine(driver, spec_htmls)
    driver.close()

    exit(fail_count)
