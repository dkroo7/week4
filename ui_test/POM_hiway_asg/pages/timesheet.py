import time
from POM_hiway_asg.pages.login_using_google import LoginWithGoogle as LWG
from POM_hiway_asg.pages.hiway_homepage import HiwayHomepageOptions
from POM_hiway_asg.pages.constant_var import *
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import date, timedelta
from POM_hiway_asg.test_scripts.base import BasePage


class TimesheetOptions(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def login_goto_timesheet(self):
        driver = self.driver
        login_page = LWG(driver)
        login_page.login_hiway()
        hiway_homepage = HiwayHomepageOptions(driver)
        time.sleep(2)  # the page needed the API call to complete, but the API is taking time
        hiway_homepage.click_timesheet_tab()

    def delete_timesheet_entry(self):
        driver = self.driver
        try:
            driver.find_element_by_css_selector(DELETE_BIN_ICON).click()
            time.sleep(5)  # the page needed the API call to complete, but the API is taking time
            return True
        except:
            return False

    def delete_all_timesheet_entry(self):
        driver = self.driver
        timesheet_entries = driver.find_elements_by_name(TIMESHEET_HOUR_FIELD_NAME)
        for entry in timesheet_entries:
            driver.find_element_by_css_selector(DELETE_BIN_ICON).click()
            time.sleep(5)  # page needed the API call to complete, but the API is taking time

    def make_timesheet_entry(self, task_code, task_type, task_hour, task_min, task_dsc):
        driver = self.driver
        driver.find_element_by_id(TIMESHEET_PROJECT_CODE_IDENTIFIER).clear()
        driver.find_element_by_id(TIMESHEET_PROJECT_CODE_IDENTIFIER).send_keys(
            task_code + Keys.TAB + task_type + Keys.TAB + task_hour + Keys.TAB + task_min + Keys.TAB + task_dsc + Keys.RETURN)
        time.sleep(5)  # using this sleep because the page needed the API call to complete, but the API is taking time

    def read_timesheet_time(self):
        timesheet_time = self.driver.find_element_by_css_selector(TIMESHEET_TIME_SELECTOR).text
        return timesheet_time

    def verify_default_date_is_today(self):
        timesheet_time = self.read_timesheet_time()
        timesheet_date = timesheet_time[-6:]
        if timesheet_date == TODAY_DATE:
            return True
        else:
            return False

    def verify_total_work_time(self):
        timesheet_entries = self.driver.find_elements_by_name(TIMESHEET_HOUR_FIELD_NAME)
        hour_total = 0
        min_total = 0
        count = 0
        for timesheet_entry in timesheet_entries:
            min_end_text = ',"project_code"'
            if count > 0:
                min_end_text = ',"description'
            count = 1
            entry = timesheet_entry.get_attribute(TIMESHEET_ENTRY_ATTRIBUTE)
            hour_start = entry.find('"hrs":') + 6
            hour_end = entry.find(',"min":')
            hour_total += int(entry[hour_start:hour_end])
            min_start = entry.find('"min":') + 6
            min_end = entry.find(min_end_text)
            min_total += int(entry[min_start:min_end])

        # adding all the time of the timesheet page and converting it to minutes

        total_mins = min_total + hour_total * 60
        timesheet_time = self.read_timesheet_time()
        timesheet_hour = int(timesheet_time[:2])
        timesheet_min = int(timesheet_time[3:5])
        timesheet_total_mins = timesheet_hour * 60 + timesheet_min
        if timesheet_total_mins == total_mins:
            return total_mins, True
        return total_mins, False

    def status_of_next_btn_on_today_date(self):
        driver = self.driver
        if driver.find_element_by_xpath(TIMESHEET_NEXT_BTN_XPATH).is_enabled():
            return True
        return False

    def verify_previous_btn_click(self, click_count):
        driver = self.driver
        for click in range(click_count):
            driver.find_element_by_xpath(TIMESHEET_PREVIOUS_BTN_XPATH).click()
        timesheet_time = self.read_timesheet_time()
        timesheet_date = timesheet_time[-6:]
        prev_date = date.today() - timedelta(click_count)
        prev_date = prev_date.strftime('%b %d')
        if prev_date == timesheet_date:
            return True
        return False

    def verify_task_entry_adding(self, task_code, task_type, task_hour, task_min, task_dsc):
        driver = self.driver
        self.make_timesheet_entry(task_code, task_type, task_hour, task_min, task_dsc)
        task_data = driver.find_element_by_name(TIMESHEET_HOUR_FIELD_NAME).get_attribute(TIMESHEET_ENTRY_ATTRIBUTE)
        get_task_code = task_data[task_data.find('code":"') + 7:task_data.find('","type')]
        get_task_type = task_data[task_data.find('type":"') + 7:task_data.find('","description')]
        get_task_hour = task_data[task_data.find('"hrs":') + 6:task_data.find(',"min"')]
        get_task_min = task_data[task_data.find('"min":') + 6:task_data.find(',"project')]
        get_task_dsc = task_data[task_data.find('description":"') + 14:task_data.find('","state"')]
        if task_code == get_task_code and task_type == get_task_type and task_hour == get_task_hour and task_min == get_task_min and task_dsc == get_task_dsc:
            return True
        return False

    def taskbar_color(self):
        return self.driver.find_element_by_xpath(TIMESHEET_BAR_COLOR_XPATH).value_of_css_property('background-color')

    def verify_taskbar_color(self, hour, color):
        if hour < 8:
            dict_color_index = 1  # index for hour range 1 to 7 hours
        elif hour < 10:
            dict_color_index = 8  # index for hour range 8 to 9 hours
        else:
            dict_color_index = 10  # index for hour range 10 to 24 hours
        if color == COLORS_FOR_HOUR_RANGE_IN_PROGRESS_BAR[dict_color_index]:
            return True
        return False

    def add_btn_status(self):
        driver = self.driver
        return driver.find_element_by_xpath(TIMESHEET_ADD_BTN_XPATH).is_enabled()

    def verify_enrty_freez(self):
        driver = self.driver
        return len(driver.find_element_by_id(TIMESHEET_PROJECT_CODE_IDENTIFIER)) == 0

    def verify_msg_to_make_entry(self):
        driver = self.driver
        try:
            msg_text = driver.find_element_by_xpath(TIMESHEET_NO_ENTRY_MSG_XPATH).text
            if msg_text == MSG_TO_MAKE_ENTRY_TEXT:
                return True
            return False
        except NoSuchElementException:
            return False

    def check_username(self, username):
        driver = self.driver
        header_text = driver.find_element_by_xpath(TIMESHEET_USERNAME_XPATH).text
        if header_text.find(username):
            return True
        return False
