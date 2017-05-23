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


class Navigation(KeywordGroup):
    def go_to_page(self, xml_path):
        """
        Will navigate to the page based on the XML path.

        Example:
        | Go To Page | `Some XML String` |
        """

        self.builtIn.wait_until_keyword_succeeds(self.action_timeout,
                                                 self.action_retry_interval,
                                                 "internal_go_to_page",
                                                 xml_path)

    def internal_go_to_page(self, xmlPath):
        """Will navigate to the page based on the XML path.

        Example:
        | Go To Page | `Some XML String` |
        """
        appendedVariable = xmlPath.split("|")
        pathSteps = appendedVariable[0].split("/")
        logger.debug("Going to Page: %s" % xmlPath)
        navPage = ""
        for step in pathSteps:
            if step != "":
                logger.debug("Going to next step: %s" % step)
                navPage += ("/%s" % step)

                self.change_page_view(navPage)
                self.click(step, step)

    def focus(self, name):
        """
        Sets focus to the `name`.
        """
        validTypes = ["button", "checkbox", "element", "image", "radio_button", "link", "textfield", "list",
                      "list_input", "input", "secret"]

        locatorValues = self._ui_data(name, validTypes)

        self._wait_for_element(locatorValues["locator"])

        # print locatorValues["locator"]
        # self.seleniumlib.focus(locatorValues["locator"])

        if self.webDriver.capabilities['browserName'] == 'firefox' \
                and self.webDriver.capabilities['version'] > '34':
            if locatorValues["locator"][:5] != 'xpath':
                javascript = (('document.getElementById("%s").focus();') % (locatorValues["locator"]))
                self.seleniumlib.execute_javascript(javascript)
        else:
            self.seleniumlib.focus(locatorValues["locator"])

            # print javascript
            # javascript = (("document.getElementsByName('%s')[0].focus()") % (locatorValues['locator']))
            # self.seleniumlib.execute_javascript(javascript)

    def scroll_page(self, yTarget=0, xTarget=0):
        """
        Scrolls the page to specified location
        Takes in an optional arguments as % of the page to scroll to
        """

        javascript = "window.scrollTo(%f * document.body.scrollWidth, %f * document.body.scrollHeight);" % (
            float(xTarget) / 100, float(yTarget) / 100)
        self.seleniumlib.execute_javascript(javascript)
