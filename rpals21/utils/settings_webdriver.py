import os
import sys

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# configuring the chrome driver for platform
BASE_DIR = os.path.dirname(__file__)


def get_executable_path():
    if sys.platform == 'linux':
        executable_path = os.path.join(BASE_DIR, 'drivers', 'chromedriver')
    elif sys.platform == 'mac':
        executable_path = os.path.join(BASE_DIR, 'drivers', 'chromedriver')
    else:
        executable_path = os.path.join(BASE_DIR, 'drivers', 'chromedriver.exe')
    return executable_path


get_executable_path()

# creating configurations to the driver
options = Options()
options.add_argument('start-maximized')
options.add_argument('--incognito')

driver: WebDriver = WebDriver(
    executable_path=get_executable_path(),
    options=options
)


# creating an explicit wait driver
driver_wait = WebDriverWait(driver=driver, timeout=20)


def get_element(by, value):
    return driver_wait.until(EC.element_to_be_clickable((by, value)))