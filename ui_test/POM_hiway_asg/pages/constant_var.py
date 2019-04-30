import os
from datetime import date

CHROME_DRIVER_PATH = 'chromedriver_linux64/chromedriver'
USER_ENTRY_PATH = 'pages/user_timesheet_entry_details.csv'
PROJECT_PATH = os.getcwd()
POM_HIWAY_ASG_PATH, NOT_STORING_VALUE = os.path.split(PROJECT_PATH)
USER_ENTRY_DETAILS_CSV = os.path.join(POM_HIWAY_ASG_PATH, USER_ENTRY_PATH)
UI_TEST_PATH, NOT_STORING_VALUE = os.path.split(POM_HIWAY_ASG_PATH)
WEBDRIVER_PATH = os.path.join(UI_TEST_PATH, CHROME_DRIVER_PATH)

TODAY_DATE = date.today().strftime('%b %d')

TESTING_WEBSITE_URL = 'https://qa.hiway.hashedin.com/'

ORANGE_COLOR = 'rgba(255, 87, 34, 1)'
BLUE_COLOR = 'rgba(63, 81, 181, 1)'
PINK_COLOR = 'rgba(255, 64, 129, 1)'

COLORS_FOR_HOUR_RANGE_IN_PROGRESS_BAR = {1: ORANGE_COLOR, 8: BLUE_COLOR, 10: PINK_COLOR}

MSG_TO_MAKE_ENTRY_TEXT = 'No Time Entries. Use the form below to add one.'

VALID_USERNAME_LOGIN = 'deepesh.kumar@hashedin.com'
VALID_PASSWORD_LOGIN = '211011218092161496'
INVALID_USERNAME_LOGIN = 'not_valid@hashedin.com'
INVALID_PASSWORD_LOGIN = 'YOYOYOYO'
USER_NAME = 'Deepesh Kumar'

TIMESHEET_TAB_BTN = '//a[contains(.,"TimeSheet")]'
LOGIN_WITH_GOOGLE_BTN = '//a[contains(.,"Google")]'
USER_NAME_IDENTIFIER = 'identifierId'
PASSWORD_IDENTIFIER = 'password'
START_USING_HIWAY_BTN = '.h3.btn'
DELETE_BIN_ICON = '.md-warn.ng-scope.material-icons'
TIMESHEET_PROJECT_CODE_IDENTIFIER = 'input-20'
TIMESHEET_TIME_SELECTOR = '.mobile-timesheet-date.ng-binding'
TIMESHEET_HOUR_FIELD_NAME = 'entry.hrs'
TIMESHEET_ENTRY_ATTRIBUTE = 'ng-change'
TIMESHEET_NEXT_BTN_XPATH = '//button[@type="button" and @ng-click="next()"]'
TIMESHEET_PREVIOUS_BTN_XPATH = '//button[@type="button" and @ng-click="prev()"]'
TIMESHEET_BAR_COLOR_XPATH = '//div[@class="md-bar md-bar2"]'
TIMESHEET_ADD_BTN_XPATH = '//div[@class="md-bar md-bar2"]'
TIMESHEET_NO_ENTRY_MSG_XPATH = '//div[@ng-if="timeEntry.length == 0"]/i'
TIMESHEET_USERNAME_XPATH = '//div[@class="md-title mobile-heading layout-align-center-center layout-row"]/h2'
