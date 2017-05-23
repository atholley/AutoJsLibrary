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
import os

class Browser(KeywordGroup):

    def open_browser(self, uiXmlFile, browser='firefox', alias=None, remote_url=False,
                     desired_capabilities=None, ff_profile_dir=None, default_frame=False,
                     enable_auto_visual_checks=False, enable_accessibility_checks=False):
        """
        Opens a new browser instance with given UI XML Map.

        Returns the index of this browser instance which can be used later to
        switch back to it. Index starts from 1 and is reset back to it when
        `Close All Browsers` keyword is used. See `Switch Browser` for
        example.

        Optional alias is an alias for the browser instance and it can be used
        for switching between browsers (just as index can be used). See `Switch
        Browser` for more details.

        Possible values for `browser` are as follows:

        | firefox          | FireFox   |
        | ff               | FireFox   |
        | internetexplorer | Internet Explorer |
        | ie               | Internet Explorer |
        | googlechrome     | Google Chrome |
        | gc               | Google Chrome |
        | chrome           | Google Chrome |
        | opera            | Opera         |
        | phantomjs        | PhantomJS     |
        | htmlunit         | HTMLUnit      |
        | htmlunitwithjs   | HTMLUnit with Javascipt support |
        | android          | Android       |
        | iphone           | Iphone        |
        | safari           | Safari        |

        Note, that you will encounter strange behavior, if you open
        multiple Internet Explorer browser instances. That is also why
        `Switch Browser` only works with one IE browser at most.
        For more information see:
        http://selenium-grid.seleniumhq.org/faq.html#i_get_some_strange_errors_when_i_run_multiple_internet_explorer_instances_on_the_same_machine

        Optional 'remote_url' is the url for a remote selenium server for example
        http://127.0.0.1/wd/hub.  If you specify a value for remote you can
        also specify 'desired_capabilities' which is a string in the form
        key1:val1,key2:val2 that will be used to specify desired_capabilities
        to the remote server. This is useful for doing things like specify a
        proxy server for internet explorer or for specify browser and os if your
        using saucelabs.com. 'desired_capabilities' can also be a dictonary
        (created with 'Create Dictionary') to allow for more complex configurations.

        Optional 'ff_profile_dir' is the path to the firefox profile dir if you
        wish to overwrite the default.
        """

        if remote_url:
            self.seleniumlib._info("Opening browser '%s' through remote server at '%s'"
                                   % (browser, remote_url))
        else:
            self.seleniumlib._info("Opening browser '%s'" % browser)


        if enable_accessibility_checks == True:
            ff_profile_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'profile')
            browser ='firefox'

        browser_name = browser
        browser = self.seleniumlib._make_browser(browser_name=browser, desired_capabilities=desired_capabilities, profile_dir=ff_profile_dir, remote=remote_url)
        self.seleniumlib._debug('Opened browser with session id %s'
                                % browser.session_id)

        alias = self.seleniumlib._cache.register(browser, alias)

        if browser_name not in ['android', 'iphone']:
            self.seleniumlib.maximize_browser_window()

        self.set_ui_map(uiXmlFile)

        self.builtIn.set_global_variable("${DYNAMIC_FRAME_ID}", None)

        if default_frame:
            self.default_frame = default_frame
        else:
            self.default_frame = False

        # Sets
        delay = self.builtIn.get_variable_value("${DELAY}")
        if delay != 0:
            self.seleniumlib.set_selenium_speed(delay)
            print delay

        # Create a global variable for use to identify what browser is in use.
        self.webDriver = self.seleniumlib._current_browser()

        # Enables automated visual checks on Click
        self.visual_checks = enable_auto_visual_checks
        return alias

    def close_all_browsers(self):
        """
        Closes all open browsers and resets the browser cache.

        After this keyword new indexes returned from `Open Browser` keyword
        are reset to 1.

        This keyword should be used in test or suite teardown to make sure
        all browsers are closed.
        """
        self.seleniumlib.close_all_browsers()

    def capture_page_screenshot(self):
        """Takes screenshot of the current page"""
        self.seleniumlib.capture_page_screenshot()
