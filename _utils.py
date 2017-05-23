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


'''
    def wait_until_page_contains_custom(self, xmlLocator, text, keywordToReloadPage):
        """ Waits until `text` appears on current page based on element identifed in `xmlLocator`.
            Additionally the base will be reloaded by using the keyword passed by `keywordToReloadPage`.

            Exmaple,
            | Wait Until Page Contains Custom | `Some Text` | `Some Keyword` |
        """
        elementValue = self.get_text_custom(xmlLocator)
        counter = 0
        while(elementValue != text):
            self.builtIn.run_keyword(keywordToReloadPage)
            self.builtIn.sleep(5) # Sleeps for 5 seconds
            elementValue = self.get_text_custom(xmlLocator)
            logger.info("Element Value %s" % elementValue)
            counter += 1
            if (elementValue == text):
                self.seleniumlib.capture_page_screenshot()
                break
            elif (elementValue == "Error"):
                self.seleniumlib.capture_page_screenshot()
                raise ValueError("An error has occured!")
            elif (elementValue == "Queued") and (counter == 5):
                self.seleniumlib.capture_page_screenshot()
                break
            elif (counter > 120):
                self.seleniumlib.capture_page_screenshot()
                raise ValueError(("Expected value %s is not on screen") % (text))
            else:
                continue
    def _log_url_to_tracking_file(self):

        logUrls = self.builtIn.get_variable_value('${logUrls}')

        if logUrls == "Enabled":
            uiXmlContext = self.builtIn.get_variable_value('${uiXmlContext}')
            currentUrl = self.seleniumlib.get_location()
            suite = self.builtIn.get_variable_value('${SUITE_SOURCE}')
            test = self.builtIn.get_variable_value('${TEST_NAME}')

            fileName = os.path.join(os.path.expanduser('~'), "pageCoverage.csv")
            fo = open(fileName, "ab")
            #self.builtIn.log((("Appending to File: %s") % (fileName)), "INFO")

            baseUrl = self.__trunc_at(currentUrl, "/" , 3)
            baseApp = self.__trunc_at(currentUrl, "/" , 4)
            app = baseApp[len(baseUrl)+1:]
            url = currentUrl[len(baseApp):]

            fileLine = (("%s,%s,%s,%s,%s,%s\r\n") %(uiXmlContext, suite, test, currentUrl, app, url))
            fo.write(fileLine)
            fo.close()
'''
