import pytest
from selenium import webdriver
from POM_hiway_asg.pages.constant_var import *


@pytest.yield_fixture
def setUp():
    browser = webdriver.Chrome(WEBDRIVER_PATH)
    browser.get(TESTING_WEBSITE_URL)
    browser.maximize_window()
    browser.implicitly_wait(10)
    yield browser
    browser.close()
