import time
from POM_hiway_asg.pages.constant_var import TIMESHEET_TAB_BTN


class HiwayHomepageOptions():

    def __init__(self, driver):
        self.driver = driver

    def click_timesheet_tab(self):
        time.sleep(5)  # using this sleep because the page needed the API call to complete, but the API is taking time
        self.driver.find_element_by_xpath(TIMESHEET_TAB_BTN).click()
