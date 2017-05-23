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


class Click(KeywordGroup):
    def click(self, name, pageView, pageCheckText=None):
        """
        Clicks an item identified by `name`.
        Changes page view to `pageView` value.
        Waits until `pageCheckText` is found.
        """

        validTypes = ["link", "image", "element", "url", "button"]
        locatorValues = self._ui_data(name, validTypes)

        self.internal_wait_until_keyword_succeeds('internal_click',
                                                  locatorValues,
                                                  name,
                                                  pageView,
                                                  pageCheckText)

        self._frame_mgt(locatorValues, "page_contains")

        self.internal_wait_until_keyword_succeeds('internal_wait_until_page_contains',
                                                  locatorValues)

        # self.wait_until_page_contains(locatorValues)

        self._frame_mgt(locatorValues, "last")

        self.change_page_view(pageView)

        #if self.visual_checks == True:
        #    self.check_eyes_window(pageView, force_full_page_screenshot=True)

    def internal_click(self, locatorValues, name, pageView, pageCheckText):
        """
        Internal click keyword that is used by `click`.
        """

        # get modifier attribute for the first matching tag
        modifierAttribute = self.get_data_ui_xml_value(name)[0]['modifier']

        if pageCheckText is not None:
            locatorValues["pageCheck"] = pageCheckText

        if locatorValues["pageCheck"] is None:
            raise Exception("No page check has been specified!")

        if locatorValues["type"] == "url":
            logger.debug("Running url type commands")

            url = locatorValues["locator"]

            logger.info("Going to url: %s" % url)
            self.seleniumlib.go_to(url)

        else:
            self._frame_mgt(locatorValues)

            if locatorValues["type"] == "link":
                if locatorValues["locator"][:5] == "xpath" \
                        or locatorValues["locator"][:3] == "id=" \
                        or locatorValues["locator"][:4] == "css=" \
                        or locatorValues["locator"][:13] == "partial link=":
                    self._wait_for_element(locatorValues["locator"], modifierAttribute)
                else:
                    self._wait_for_element("link=%s" % locatorValues["locator"], modifierAttribute)
            else:
                self._wait_for_element(locatorValues["locator"], modifierAttribute)

            if locatorValues["modifier"] == "focus":
                self._stale_element("focus", (locatorValues["locator"]))
            elif locatorValues["modifier"] == "hover":
                self._stale_element("mouse_over", (locatorValues["locator"]))

            elif locatorValues["modifier"] == "double":
                self._stale_element("click_%s" % locatorValues["type"], locatorValues["locator"])
                self._stale_element("click_%s" % locatorValues["type"], locatorValues["locator"])
            elif locatorValues["modifier"] == "hidden" \
                    and self.webDriver.capabilities['browserName'] != 'safari' \
                    and self.webDriver.capabilities['version'] != '5.1.9':
                javascript = (('document.getElementById("%s").click();') % (locatorValues["locator"]))
                self.seleniumlib.execute_javascript(javascript)


            else:
                self._stale_element("click_%s" % locatorValues["type"], locatorValues["locator"])

            self._frame_mgt(locatorValues)
