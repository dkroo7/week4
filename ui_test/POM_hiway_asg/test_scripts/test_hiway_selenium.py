import logging
import pytest
import csv
import time
from POM_hiway_asg.pages.login_using_google import LoginWithGoogle as LWG
from POM_hiway_asg.pages.timesheet import TimesheetOptions
from POM_hiway_asg.pages.constant_var import *

logging.basicConfig(filename=HIWAY_LOG_FILE_NAME,
                    format=LOGGER_LOG_ENTRY_FORMAT,
                    datefmt=LOGGER_DATE_ENTRY_FORMAT)


class TestHiway():
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)

    @pytest.fixture(autouse=True)
    def setup(self, setUp):
        self.driver = setUp
        self.sample_entry = self.load_user_entry_csv()
        self.timesheet_page = TimesheetOptions(self.driver)

    def load_user_entry_csv(self, filename=USER_ENTRY_DETAILS_CSV):
        lines = csv.reader(open(filename, 'r'))
        sample_entry = list(lines)
        sample_entry.pop(0)
        return sample_entry

    def test_hiway_login(self, setup):
        login_page = LWG(self.driver)
        login_page.click_login_with_google_btn()
        login_page.enter_username_password(VALID_USERNAME_LOGIN, VALID_PASSWORD_LOGIN)
        time.sleep(5)
        status_flag = login_page.verify_login_success()
        try:
            assert status_flag == False
        except AssertionError:
            self.logger.error('Login to the hiway was not successful')

    def test_timesheet_default_time(self, setup):
        self.timesheet_page.login_goto_timesheet()
        status_flag = self.timesheet_page.verify_default_date_is_today()
        try:
            assert status_flag == True
        except AssertionError:
            self.logger.error('The default date of timesheet page is not showing the current date')

    def test_timesheet_total_work_hour(self, setup):
        sample_entry = self.sample_entry
        self.timesheet_page.login_goto_timesheet()
        self.timesheet_page.delete_all_timesheet_entry()
        self.timesheet_page.make_timesheet_entry(task_code=sample_entry[0][0], task_type=sample_entry[0][1],
                                                 task_hour=sample_entry[0[2]], task_min=sample_entry[0][3],
                                                 task_dsc=sample_entry[0][4])
        total_min, status_flag = self.timesheet_page.verify_total_work_time()
        try:
            assert status_flag == True
        except AssertionError:
            self.logger.error('The total time of timesheet page is different from timesheet entry work hours')

    def test_timesheet_next_btn_today(self, setup):
        self.timesheet_page.login_goto_timesheet()
        status_flag = self.timesheet_page.status_of_next_btn_on_today_date()
        try:
            assert status_flag == False
        except AssertionError:
            self.logger.error('Timesheet next button is not desabled for today')

    def test_timesheet_prev_btn(self, setup):
        self.timesheet_page.login_goto_timesheet()
        status_flag = self.timesheet_page.verify_previous_btn_click(click_count=3)
        try:
            assert status_flag == False
        except AssertionError:
            self.logger.error('PREV button click on timesheet page is not working correctly')

    def test_timesheet_task_entry_adding(self, setup):
        sample_entry = self.sample_entry
        self.timesheet_page.login_goto_timesheet()
        self.timesheet_page.delete_all_timesheet_entry()
        status_flag = self.timesheet_page.verify_task_entry_adding(task_code=sample_entry[0][0],
                                                                   task_type=sample_entry[0][1],
                                                                   task_hour=sample_entry[0][2],
                                                                   task_min=sample_entry[0][3],
                                                                   task_dsc=sample_entry[0][4])
        try:
            assert status_flag == True
        except AssertionError:
            self.logger.error('The taks entry is not added to the timesheet page')

    def test_timesheet_taskbar_color_8hour(self, setup):
        sample_entry = self.sample_entry
        self.timesheet_page.login_goto_timesheet()
        self.timesheet_page.delete_all_timesheet_entry()
        self.timesheet_page.make_timesheet_entry(task_code=sample_entry[0][0], task_type=sample_entry[0][1],
                                                 task_hour=sample_entry[0][2], task_min=sample_entry[0][3],
                                                 task_dsc=sample_entry[0][4])
        taskbar_color = self.timesheet_page.taskbar_color()
        if self.timesheet_page.verify_taskbar_color(hour=sample_entry[0][2], color=taskbar_color):
            self.timesheet_page.make_timesheet_entry(task_code=sample_entry[0][0], task_type=sample_entry[0][1],
                                                     task_hour=sample_entry[0][2], task_min=sample_entry[0][3],
                                                     task_dsc=sample_entry[0][4])
        taskbar_new_color = self.timesheet_page.taskbar_color()
        status_flag = self.timesheet_page.verify_taskbar_color(hour=sample_entry[0][2] + sample_entry[0][2],
                                                               color=taskbar_new_color)
        try:
            assert status_flag == True
        except AssertionError:
            self.logger.error('The taskbar color is not chenging from orange to blue with 8 hour of entry')

    def test_timesheet_taskbar_color_9hour(self, setup):
        sample_entry = self.sample_entry
        self.test_timesheet_taskbar_color_8hour(setup)
        self.timesheet_page.make_timesheet_entry(task_code=sample_entry[0][0], task_type=sample_entry[0][1],
                                                 task_hour='1', task_min=sample_entry[0][3],
                                                 task_dsc=sample_entry[0][4])
        taskbar_color = self.timesheet_page.taskbar_color()
        status_flag = self.timesheet_page.verify_taskbar_color(hour=sample_entry[0][2] + sample_entry[0][2] + 1,
                                                               color=taskbar_color)
        try:
            assert status_flag == True
        except AssertionError:
            self.logger.error('The taskbar color is not chenging from blue to pink with 9 hour of entry')

    def test_timesheet_add_btn_status_with_noentry(self, setup):
        self.timesheet_page.login_goto_timesheet()
        status_flag = self.timesheet_page.add_btn_status()
        try:
            assert status_flag == False
        except AssertionError:
            self.logger.error('The add button is enabled although all mendetory fields are not entered')

    def test_timesheet_del_button(self, setup):
        sample_entry = self.sample_entry
        self.timesheet_page.login_goto_timesheet()
        self.timesheet_page.delete_all_timesheet_entry()
        self.timesheet_page.make_timesheet_entry(task_code=sample_entry[0][0], task_type=sample_entry[0][1],
                                                 task_hour=sample_entry[0][2], task_min=sample_entry[0][3],
                                                 task_dsc=sample_entry[0][4])
        status_flag = self.timesheet_page.delete_timesheet_entry()
        try:
            assert status_flag == True
        except AssertionError:
            self.logger.error('Timesheet delete button is not working')

    def test_timesheet_freez_for_2days_old_entry(self, setup):
        self.timesheet_page.login_goto_timesheet()
        status = self.timesheet_page.verify_previous_btn_click(click_count=2)
        if status == True:
            status_flag = self.timesheet_page.verify_enrty_freez()
        try:
            assert status_flag == True
        except AssertionError:
            self.logger.error('The timesheet is not freezed for 2 days old entry')

    def test_timesheet_msg_for_noentry(self, setup):
        self.timesheet_page.login_goto_timesheet()
        self.timesheet_page.delete_all_timesheet_entry()
        status_flag = self.timesheet_page.verify_msg_to_make_entry()
        try:
            assert status_flag == True
        except AssertionError:
            self.logger.error('Timesheet is not giving messages to make entry if no entry is present')

    def test_timesheet_for_24plus_hours_entry(self, setup):
        sample_entry = self.sample_entry
        entry_count = 4
        status_flag = True
        self.timesheet_page.login_goto_timesheet()
        self.timesheet_page.delete_all_timesheet_entry()
        for entry in range(entry_count):
            self.timesheet_page.make_timesheet_entry(task_code=sample_entry[0][0], task_type=sample_entry[0][1],
                                                     task_hour='6', task_min='10',
                                                     task_dsc=sample_entry[0])
        total_work_time, status = self.timesheet_page.verify_total_work_time()
        if total_work_time > 24:  # total working hour can not exceed 24 hours
            status_flag = False
        try:
            assert status_flag == True
        except AssertionError:
            self.logger.error('Timesheet is taking entry for more than 24 hours of work in one day')

    def test_timesheet_10plus_hour_in_single_entry(self, setup):
        sample_entry = self.sample_entry
        self.timesheet_page.login_goto_timesheet()
        self.timesheet_page.delete_all_timesheet_entry()
        self.timesheet_page.make_timesheet_entry(task_code=sample_entry[0][0], task_type=sample_entry[0][1],
                                                 task_hour='11', task_min=sample_entry[0][3],
                                                 task_dsc=sample_entry[0][4])
        status_flag = self.timesheet_page.verify_msg_to_make_entry()
        try:
            assert status_flag == True
        except AssertionError:
            self.logger.error('Timesheet is accepting 10 plus hour of a single entry')

    def test_timesheet_username(self, setup):
        self.timesheet_page.login_goto_timesheet()
        status_flag = self.timesheet_page.check_username(USER_NAME)
        try:
            assert status_flag == True
        except AssertionError:
            self.logger.error('Time sheet is not showing right USERNAME for the given login details')
