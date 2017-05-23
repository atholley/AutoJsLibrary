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


class Select(KeywordGroup):
    def select_from(self, name, *items):
        """
        Selects `items` from list identified by `name`

        If more than one value is given for a single-selection list, the first
        value will be selected. If the target list is a multi-selection list,
        and `items` is an empty list, all values of the list will be selected.

        Valid UI Types Values: list, list_input, select2

        * Select2 UI Example *
            Select2 requires 2 ui mappings:

            First is the down arrow of the select list
                <sample_select2 type="select2">Locator Value/sample_select2>

            Second is the input box. Note you must append *_input* to the end of the UI value
                <sample_select2*_input* type="select2">Locator Value</sample_select2_input>

        """
        validTypes = ["list", "list_input", "select2"]
        locatorValues = self._ui_data(name, validTypes)

        # get modifier attribute for the first matching tag
        modifierAttribute = self.get_data_ui_xml_value(name)[0]['modifier']

        read_only_mode = self._get_read_only_mode_state()

        if locatorValues["type"] == "list_input":
            if not read_only_mode:
                self._stale_element("input_text", locatorValues["locator"], items[0])
                self._wait_for_element("link=%s" % items[0], modifierAttribute)
                self._stale_element("click_link", items[0])
            if locatorValues["modifier"] != "no_check":
                # self.should_contain_text(name, items[0])
                self.builtIn.wait_until_keyword_succeeds(locatorValues['action_timeout'],
                                                         locatorValues['action_retry_interval'],
                                                         'should_contain_text',
                                                         locatorValues["locator"],
                                                         items[0])
        if locatorValues["type"] == "list":
            if not read_only_mode:
                self._stale_element("select_from_list_by_label", locatorValues["locator"], *items)
            if locatorValues["modifier"] != "no_check":
                self.builtIn.wait_until_keyword_succeeds(locatorValues['action_timeout'],
                                                         locatorValues['action_retry_interval'],
                                                         'internal_list_selection_should_be',
                                                         locatorValues["locator"],
                                                         *items)

        if locatorValues["type"] == "select2":
            if not read_only_mode:
                self._stale_element("click_element", locatorValues["locator"])
                # locatorValues = self._ui_data(name + "_input", validTypes)
                # self._stale_element("input_text", locatorValues["locator"], items[0])
                self._stale_element("input_text", 'xpath=//input[@class="select2-search__field"]', items[0])
                # self._stale_element("click_element", 'xpath=//li[text()="%s"]' % items[0])
                self._stale_element("click_element", 'xpath=//li[@class="select2-results__option select2-results__option--highlighted"]')
                # self._stale_element.input_text('xpath=//input[@class="select2-search__field"]',value)
            if locatorValues["modifier"] != "no_check":
                self.builtIn.wait_until_keyword_succeeds(locatorValues['action_timeout'],
                                                         locatorValues['action_retry_interval'],
                                                         'should_contain_text',
                                                         name,
                                                         items[0])

                # self.should_contain_text(name, items[0])
            # self.should_be_selected(name, items[0])
    def internal_list_selection_should_be(self, name, *items):
        inputValue = self.seleniumlib.list_selection_should_be(name, *items)

    def select(self, name, action="select"):
        """
        By default selects item identified by `name`.
        Optionally: Pass select / unselect to set the desired action.
        """
        validTypes = ["checkbox", "radio_button", "element"]
        locatorValues = self._ui_data(name, validTypes)

        read_only_mode = self._get_read_only_mode_state()

        self._wait_for_element(locatorValues["locator"])

        if locatorValues["type"] == "class":
            if not read_only_mode:
                javascript = (('document.getElementsbyclassName("%s").click();') % (locatorValues["locator"]))
                self.seleniumlib.execute_javascript(javascript)

        if locatorValues["type"] == "checkbox" and action == "select":
            if not read_only_mode:
                self._stale_element("select_checkbox", locatorValues["locator"])
            if locatorValues["modifier"] != "no_check":
                #self.should_be_selected(name)
                self.builtIn.wait_until_keyword_succeeds(locatorValues['action_timeout'],
                                                         locatorValues['action_retry_interval'],
                                                         'should_be_selected',
                                                         name)

        if locatorValues["type"] == "checkbox" and action == "unselect":
            if not read_only_mode:
                self._stale_element("unselect_checkbox", locatorValues["locator"])
            if locatorValues["modifier"] != "no_check":
                # self.should_be_unselected(name)
                self.builtIn.wait_until_keyword_succeeds(locatorValues['action_timeout'],
                                                         locatorValues['action_retry_interval'],
                                                         'should_be_unselected',
                                                         name)
        if locatorValues["type"] == "radio_button":
            if not read_only_mode:
                self._stale_element("click_element", locatorValues["locator"])
                if locatorValues["modifier"] != "triple_click":
                    self._stale_element("click_element", locatorValues["locator"])
                    self._stale_element("click_element", locatorValues["locator"])
            if locatorValues["modifier"] != "no_check":
                self.builtIn.wait_until_keyword_succeeds(locatorValues['action_timeout'],
                                                         locatorValues['action_retry_interval'],
                                                         'should_be_selected',
                                                         name)

        if locatorValues["type"] == "element":
            if not read_only_mode:
                self._stale_element("click_element", locatorValues["locator"])

    def select_frame(self, name):
        """
        Explicit frame management.
        Takes in a frame locator
        """
        validTypes = ['frame']
        locatorValues = self._ui_data(name, validTypes)

        self._wait_for_element(locatorValues["locator"])
        self.seleniumlib.select_frame(locatorValues['locator'])

    def unselect_frame(self):
        """
        Explicit frame management.
        Unselects back to top level frame
        """
        self.seleniumlib.unselect_frame()
