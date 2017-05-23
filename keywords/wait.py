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


class Wait(KeywordGroup):
    def wait_until_page_contains(self, locator_value):
        """Wait until  contains a locator"""

        validTypes = "pageCheck"
        locator_values = self._ui_data(locator_value, validTypes)

        self.internal_wait_until_keyword_succeeds('internal_wait_until_page_contains',
                                                  locator_values)

    def internal_wait_until_page_contains(self, locator_values):
        """Wait until page contains an internal locator"""
        
        page_check_text = self._parse_rf_variables(locator_values["pageCheck"])

        self.seleniumlib.wait_until_page_contains(page_check_text)

    def wait_until_page_contains_element(self, locator_value):
        """Wait until page contains an element"""
        validTypes = ["button", "checkbox", "element", "image", "radio_button", "link", "textfield", "list",
                      "list_input", "input", "secret", "textarea", "text", "select2", "input_lookup"]

        locator_values = self._ui_data(locator_value, validTypes)

        self.internal_wait_until_keyword_succeeds('internal_wait_until_page_contains_element',
                                                  locator_values)

    def internal_wait_until_page_contains_element(self, locator_values):
        """Wait until page contains an internal element"""
        self.seleniumlib.wait_until_page_contains_element(locator_values["locator"])

    def wait_until_element_does_not_contain(self, locator, text, timeout=None):
        """
        Waits until given element does not contain text.
        ** Arguments **
        locator, text, timeout=None

        """
        validTypes = ["button", "checkbox", "element", "image", "radio_button", "link", "textfield", "list",
                      "list_input", "input", "secret", "textarea", "text", "select2", "input_lookup"]
        locator_values = self._ui_data(locator, validTypes)
        self.seleniumlib.wait_until_element_does_not_contain(locator_values["locator"], text, timeout)

    def wait_until_element_is_enabled(self, item):
        """
        Waits until element specified with locator is enabled.
        """
        validTypes = ["button", "checkbox", "element", "image", "radio_button", "link", "textfield", "list",
                      "list_input", "input", "secret", "textarea", "text", "select2", "input_lookup"]
        locator_values = self._ui_data(item, validTypes)
        self.seleniumlib.wait_until_element_is_enabled(locator_values["locator"])


    def wait_until_element_is_not_visible(self, locator, timeout=None, error=None):
        """
        Waits until element specified with locator is not visible.
        """
        validTypes = ["button", "checkbox", "element", "image", "radio_button", "link", "textfield", "list",
                      "list_input", "input", "secret", "textarea", "text", "select2", "input_lookup"]
        locator_values = self._ui_data(locator, validTypes)
        self.seleniumlib.wait_until_element_is_not_visible(locator_values["locator"], timeout, error)
