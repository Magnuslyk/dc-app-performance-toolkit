import random

from selenium.webdriver.common.by import By
import requests
import json
from requests.auth import HTTPBasicAuth
from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.confluence.pages.pages import Login, AllUpdates
from util.conf import CONFLUENCE_SETTINGS


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_pages']:
        app_specific_page_id = datasets['custom_page_id']

    # To run action as specific user uncomment code bellow.
    # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
    # just before test_2_selenium_z_log_out
    # @print_timing("selenium_app_specific_user_login")
    # def measure():
    #     def app_specific_user_login(username='admin', password='admin'):
    #         login_page = Login(webdriver)
    #         login_page.delete_all_cookies()
    #         login_page.go_to()
    #         login_page.wait_for_page_loaded()
    #         login_page.set_credentials(username=username, password=password)
    #         login_page.click_login_button()
    #         if login_page.is_first_login():
    #             login_page.first_user_setup()
    #         all_updates_page = AllUpdates(webdriver)
    #         all_updates_page.wait_for_page_loaded()
    #     app_specific_user_login(username='admin', password='admin')
    # measure()

    @print_timing("test-custom-app")
    def measure():
        @print_timing("test_view")
        def sub_measure():
            page.go_to_url("http://ace52d0c7418847aaad1c3da8ac2c2a9-1230775984.us-east-2.elb.amazonaws.com/confluence/plugins/confluenceuserexport/admin.action")
            #page.wait_until_visible((By.ID, "confluence-userexport-pagination-box"))  # Wait for you app-specific UI element by ID selector

        @print_timing("test_functionality")
        def sub_sub_measure():
            username = password = "admin"
            data = {
                "searchString": "",
                "activeUsers": True,
                "inActiveUsers": True,
                "pageSize": 20,
                "offset": 0
            }

            json_string = json.dumps(data)
            api_url = "{}/confluence/rest/confluenceuserexport/1.0/search".format(CONFLUENCE_SETTINGS.server_url)
            response = requests.post(api_url, data=json_string, auth=HTTPBasicAuth('{}'.format(username), '{}'.format(password)))
        sub_measure()
        sub_sub_measure()
    measure()
