"""
Copyright 15/06/2017 UNSW Testing - Abu Tholley

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from keywordgroup import KeywordGroup
import time

class Input(KeywordGroup):
    def input_text(self, name, text):
        """
        Types the given `text` into field identified by `name`.
        Examples:
        | Input Text | name | Text |

        Valid UI Types Values: input, secret, textarea, list_input, input_lookup

        """
        validTypes = "input", "secret", "textarea", "list_input", "input_lookup", "select2"
        locatorValues = self._ui_data(name, validTypes)

        self.internal_wait_until_keyword_succeeds('internal_input_text',
                                                  locatorValues,
                                                  text)

    def internal_input_text(self, locatorValues, text):
        """
        Types the given `text` into INTERNAL field identified by `name`.
        :param locatorValues: locator modifier and type. E.g. textarea, secret (password), etc.
        :param text: The text to enter into the field
        """

        read_only_mode = self._get_read_only_mode_state()

        self._wait_for_element(locatorValues["locator"])

        if locatorValues["modifier"] == "focus":
            self._stale_element("focus", (locatorValues["locator"]))

        if locatorValues["type"] == "secret":
            self._stale_element("input_text", locatorValues["locator"], text)

        if locatorValues["type"] == "textarea":
            if not read_only_mode:
                self._stale_element("input_text", locatorValues["locator"], text)
            if locatorValues["modifier"] != "no_check":
                # self.seleniumlib.textarea_should_contain(locatorValues["locator"], text)
                self.builtIn.wait_until_keyword_succeeds(locatorValues['action_timeout'],
                                                         locatorValues['action_retry_interval'],
                                                         'internal_textarea_should_contain',
                                                         locatorValues["locator"],
                                                         text)


        if locatorValues["type"] == "input":
            if not read_only_mode:
                self._stale_element("input_text", locatorValues["locator"], text)
            if locatorValues["modifier"] != "no_check":
                # self.seleniumlib.textfield_should_contain(locatorValues["locator"], text)
                self.builtIn.wait_until_keyword_succeeds(locatorValues['action_timeout'],
                                                         locatorValues['action_retry_interval'],
                                                         'internal_textfield_should_contain',
                                                         locatorValues["locator"],
                                                         text)
        if locatorValues["type"] == "list_input":
            if not read_only_mode:
                self._stale_element("input_text", locatorValues["locator"], text)
            if locatorValues["modifier"] != "no_check":
                # self.seleniumlib.textfield_should_contain(locatorValues["locator"], text)
                self.builtIn.wait_until_keyword_succeeds(locatorValues['action_timeout'],
                                                         locatorValues['action_retry_interval'],
                                                         'internal_textfield_should_contain',
                                                         locatorValues["locator"],
                                                         text)
        if locatorValues["type"] == "input_lookup":
            if not read_only_mode:
                self._stale_element("input_text", locatorValues["locator"], text)
                self._stale_element("click_element", 'xpath=//li[text()="%s"]' % text)
            if locatorValues["modifier"] != "no_check":
                # inputValue = self.seleniumlib.get_text(locatorValues["locator"])
                # self.builtIn.should_be_equal_as_strings(inputValue, text)
                self.builtIn.wait_until_keyword_succeeds(locatorValues['action_timeout'],
                                                         locatorValues['action_retry_interval'],
                                                         'internal_list_should_contain',
                                                         locatorValues["locator"],
                                                         text)
        if locatorValues["type"] == "select2":
            if not read_only_mode:
                self._stale_element("input_text", locatorValues["locator"], text)
                self.builtIn.sleep(3)
                self._stale_element("click_element", "xpath=html/body/ul/li")
            if locatorValues["modifier"] != "no_check":
                # inputValue = self.seleniumlib.get_text(locatorValues["locator"])
                # self.builtIn.should_be_equal_as_strings(inputValue, text)
                self.builtIn.wait_until_keyword_succeeds(locatorValues['action_timeout'],
                                                         locatorValues['action_retry_interval'],
                                                         'internal_list_should_contain',
                                                         locatorValues["locator"],
                                                         text)

    def internal_textfield_should_contain(self, name, text):
        self.seleniumlib.textfield_should_contain(name, text)

    def internal_textarea_should_contain(self, name, text):
        self.seleniumlib.textarea_should_contain(name, text)

    def internal_list_should_contain(self, name, text):
        inputValue = self.seleniumlib.get_text(name)
        self.builtIn.should_be_equal_as_strings(inputValue, text)

    def choose_file(self, name, file_path):
        """
        Inputs the file_path into file input field found by identifier.
        """
        validTypes = "input", "secret", "textarea", "list_input"
        locatorValues = self._ui_data(name, validTypes)

        self._wait_for_element(locatorValues["locator"])

        self.seleniumlib.choose_file(locatorValues["locator"], file_path)

    def execute_javascript_custom(self, code):
        """
        Runs supplied javascript code
        """

        return self.seleniumlib.execute_javascript(code)

    def get_window_titles_custom(self):

        return self.seleniumlib.get_window_titles()

    def select_window_custom(self, title):

        self.seleniumlib.select_window(title)
