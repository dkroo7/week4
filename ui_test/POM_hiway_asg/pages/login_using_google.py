from POM_hiway_asg.pages.constant_var import LOGIN_WITH_GOOGLE_BTN, USER_NAME_IDENTIFIER, PASSWORD_IDENTIFIER, \
    START_USING_HIWAY_BTN, TIMESHEET_TAB_BTN, VALID_USERNAME_LOGIN, VALID_PASSWORD_LOGIN
from selenium.webdriver.common.keys import Keys
from POM_hiway_asg.test_scripts.base import BasePage


class LoginWithGoogle(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def click_login_with_google_btn(self):
        self.driver.find_element_by_xpath(LOGIN_WITH_GOOGLE_BTN).click()

    def enter_username_password(self, username, password):
        self.driver.find_element_by_id(USER_NAME_IDENTIFIER).send_keys(username + Keys.RETURN)
        self.driver.find_element_by_name(PASSWORD_IDENTIFIER).send_keys(password + Keys.RETURN)
        self.driver.find_element_by_css_selector(START_USING_HIWAY_BTN).click()

    def verify_login_success(self):
        return len(self.driver.find_element_by_xpath(TIMESHEET_TAB_BTN)) != 0

    def login_hiway(self):
        self.click_login_with_google_btn()
        self.enter_username_password(VALID_USERNAME_LOGIN, VALID_PASSWORD_LOGIN)
