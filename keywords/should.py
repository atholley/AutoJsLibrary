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
from robot.api import logger


class Should(KeywordGroup):
    def should_contain_text(self, name, expected):
        """
        Verifies the `name` contains text `expected`.

        Valid UI Map Type Values: input, textarea, element, select2, input_lookup

        """
        validTypes = ["input", "textarea", "element", "select2", "input_lookup"]
        locatorValues = self._ui_data(name, validTypes)
        self._wait_for_element(locatorValues["locator"])

        if locatorValues["type"] == "input":
            inputValue = self.seleniumlib.get_value(locatorValues["locator"])
            self.builtIn.should_be_equal_as_strings(inputValue, expected)

        if locatorValues["type"] == "textarea":
            self.seleniumlib.textarea_should_contain(locatorValues["locator"], expected)

        # TODO: Add or instead of repeating code
        if locatorValues["type"] == "input_lookup":
            inputValue = self.seleniumlib.get_value(locatorValues["locator"])
            self.builtIn.should_be_equal_as_strings(inputValue, expected)

        if locatorValues["type"] == "element":
            inputValue = self.seleniumlib.get_text(locatorValues["locator"])
            self.builtIn.should_be_equal_as_strings(inputValue, expected)

        # TODO: Add or instead of repeating code
        if locatorValues["type"] == "select2":
            inputValue = self.seleniumlib.get_text(locatorValues["locator"])
            self.builtIn.should_be_equal_as_strings(inputValue, expected)

    def should_not_contain_text(self, name, unexpected):
        """
        Verifies the `name` does not contain text `unexpected`.
        """
        validTypes = ["input", "textarea", "select2", "input_lookup"]
        locatorValues = self._ui_data(name, validTypes)
        self._wait_for_element(locatorValues["locator"])

        if locatorValues["type"] == "input" or locatorValues["type"] == "input_lookup":
            inputValue = self.seleniumlib.get_value(locatorValues["locator"])
            self.builtIn.should_not_be_equal_as_strings(inputValue, unexpected)

        if locatorValues["type"] == "textarea":
            inputValue = self.seleniumlib.get_value(locatorValues["locator"])
            self.builtIn.should_not_be_equal_as_strings(inputValue, unexpected)

        if locatorValues["type"] == "select2":
            inputValue = self.seleniumlib.get_text(locatorValues["locator"])
            self.builtIn.should_not_be_equal_as_strings(inputValue, unexpected)

    def _should_common_values(self, function, locatorValues, name, *items):
        """Internal function that is used for simple library calls."""
        self._stale_element("%s" % function, locatorValues["locator"])

    def _should_common(self, function, validTypes, name, *items):
        """Internal function that is used for simple library calls."""
        locatorValues = self._ui_data(name, validTypes)
        self._wait_for_element(locatorValues["locator"], locatorValues["modifier"])
        self._stale_element("%s" % function, locatorValues["locator"])

    def page_should_contain_text(self, text, timeout=None, retry_interval=None):
        """Verifies that current page contains `text`."""
        self.seleniumlib.page_should_contain(text)

        if timeout is None:
            timeout = self.action_timeout
        if retry_interval == None:
            retry_interval = self.action_retry_interval

        self.builtIn.wait_until_keyword_succeeds(timeout,
                                                 retry_interval,
                                                 'internal_page_should_contain_text',
                                                 text)

    def internal_page_should_contain_text(self, text):
        self.seleniumlib.page_should_contain(text)

    def page_should_not_contain_text(self, text, timeout=None, retry_interval=None):
        """
        Verifies that current page does not contain `text`.

        Optional Arguments are:
            timeout: How long we should wait
            retry_interval: How often we should check

        *Examples:*
        | Page Should Not Contain Text | Nothing | 20 seconds | 2 seconds |
        """
        if timeout is None:
            timeout = self.action_timeout
        if retry_interval is None:
            retry_interval = self.action_retry_interval

        self.builtIn.wait_until_keyword_succeeds(timeout,
                                                 retry_interval,
                                                 'internal_page_should_not_contain_text',
                                                 text)

    def internal_page_should_not_contain_text(self, text):
        self.seleniumlib.page_should_not_contain(text)

    def should_be_unselected(self, name):
        """Verifies that `name` is unselected."""
        validTypes = ["checkbox", "list", "radio_button"]
        locatorValues = self._ui_data(name, validTypes)

        if locatorValues["type"] == "checkbox":
            self._should_common("checkbox_should_not_be_selected", validTypes, name)

        if locatorValues["type"] == "list":
            self._stale_element("list_should_have_no_selections",
                                locatorValues["locator"])

        if locatorValues["type"] == "radio_button":
            result = self.seleniumlib.get_element_attribute("%s@checked" % locatorValues["locator"])
            if result is not None:
                raise Exception("%s is selected" % name)
            else:
                logger.info("%s is not selected" % name)

    def should_be_selected(self, name, *items):
        """Verifies that `name` is selected."""
        validTypes = ["checkbox", "list", "radio_button"]
        locatorValues = self._ui_data(name, validTypes)

        if locatorValues["type"] == "checkbox":
            self._stale_element("checkbox_should_be_selected",
                                locatorValues["locator"])

        if locatorValues["type"] == "list":
            stringItems = ",".join(items)
            self._stale_element("list_selection_should_be",
                                locatorValues["locator"],
                                stringItems)

        if locatorValues["type"] == "radio_button":
            result = self.seleniumlib.get_element_attribute("%s@checked" % locatorValues["locator"])
            if result != "true":
                raise Exception("%s is not selected" % name)
            else:
                logger.info("%s is selected" % name)

    def should_be_visible(self, name):
        """Verifies that `name` is visible."""
        validTypes = ["button", "checkbox", "element", "image", "radio_button", "link", "textfield", "list",
                      "list_input", "input", "secret", "textarea", "text", "select2", "input_lookup"]

        self._should_common("element_should_be_visible", validTypes, name)

    def should_be_disabled(self, name):
        """Verifies that `name` is disabled."""
        validTypes = ["button", "checkbox", "element", "image", "radio_button", "link", "textfield", "list",
                      "list_input", "input", "secret", "textarea", "text", "select2", "input_lookup"]

        self._should_common("element_should_be_disabled", validTypes, name)

    def should_be_enabled(self, name):
        """Verifies that `name` is enabled."""
        validTypes = ["button", "checkbox", "element", "image", "radio_button", "link", "textfield", "list",
                      "list_input", "input", "secret", "textarea", "text", "select2", "input_lookup"]

        self._should_common("element_should_be_enabled", validTypes, name)

    def should_not_be_visible(self, name):
        """
        Clicks a item identified by `name`.
        Changes page view to `pageView` value.
        Waits until `pageCheckText` is found.
        """
        validTypes = ["button", "checkbox", "element", "image", "radio_button", "link", "textfield", "list",
                      "list_input", "input", "secret", "textarea", "text", "select2", "input_lookup"]
        locatorValues = self._ui_data(name, validTypes)

        self.internal_wait_until_keyword_succeeds('internal_should_not_be_visible',
                                                  locatorValues,
                                                  name)

    def internal_should_not_be_visible(self, locatorValues, name):
        """Verifies that `name` is visible."""
        self._should_common_values("element_should_not_be_visible", locatorValues, name)

    def page_should_contain(self, item):
        """Verifies that current page contains `item`."""
        validTypes = ["button", "checkbox", "element", "image", "radio_button", "link", "textfield", "list",
                      "list_input", "input", "secret", "textarea", "text", "select2", "input_lookup"]
        locatorValues = self._ui_data(item, validTypes)

        self.internal_wait_until_keyword_succeeds('internal_page_should_contain',
                                                  locatorValues)

    def internal_page_should_contain(self, locatorValues):
        """Verifies that current page contains `item`."""
        if locatorValues["type"] == "list_input" or locatorValues["type"] == "input":
            self._stale_element("page_should_contain_textfield",
                                locatorValues["locator"])

        elif locatorValues["type"] == "secret" or locatorValues["type"] == "textarea":
            self._stale_element("page_should_contain_element",
                                locatorValues["locator"])
        else:
            self._stale_element("page_should_contain_%s" % locatorValues["type"],
                                locatorValues["locator"])

    def page_should_not_contain(self, item):
        """Verifies that current page does not contains `item`."""
        validTypes = ["button", "checkbox", "element", "image", "radio_button", "link", "textfield", "list",
                      "list_input",
                      "input", "secret", "textarea", "text"]
        locatorValues = self._ui_data(item, validTypes)

        self.internal_wait_until_keyword_succeeds('internal_page_should_not_contain',
                                                  locatorValues)

    def internal_page_should_not_contain(self, locatorValues):
        """Verifies that current page does not contains `item`."""
        if locatorValues["type"] == "list_input":
            self._stale_element("page_should_not_contain_textfield",
                                locatorValues["locator"])

        elif locatorValues["type"] == "secret" or locatorValues["type"] == "textarea":
            self._stale_element("page_should_not_contain_element",
                                locatorValues["locator"])
        else:
            self._stale_element("page_should_not_contain_%s" % locatorValues["type"],
                                locatorValues["locator"])
