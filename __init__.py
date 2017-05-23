'''
### Open source license ###
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
'''

import os
from keywords import *
from ExtendedSelenium2Library import ExtendedSelenium2Library
from robot.libraries.BuiltIn import BuiltIn
from _strategies import CustomStrategies
from _uimap import UiMap

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
execfile(os.path.join(THIS_DIR, 'version.py'))

__version__ = VERSION


class Web2Library(Browser,
                  Click,
                  Data,
                  Input,
                  Navigation,
                  Select,
                  Should,
                  Wait,
                  CustomStrategies,
                  UiMap,
                  RobotAppEyes):
    """
    This class initializes Selenium2Library for browser tests. It also gathers system paths, timeouts, etc to configure
    Selenium.
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self, root_dir=None, resource_dir=None, timeout=15.0,
                 implicit_wait=0.0, run_on_failure='Capture Page Screenshot', action_timeout='2 min',
                 action_retry_interval='5 sec'):

        if root_dir == None:
            root_dir = os.path.abspath(os.path.join(__file__, '..', '..'))

        if resource_dir == None:
            resource_dir = os.path.abspath(os.path.join(__file__, '..', '..'))

        # Get an instance of libraries used
        self.builtIn = BuiltIn()
        self.seleniumlib = Selenium2Library(timeout, implicit_wait, run_on_failure)

        # Get the base working directory
        self.root_dir = root_dir.replace("\\", "/")

        # Get the directory that stores the test environment resources
        if resource_dir != None:
            self.resource_dir = resource_dir.replace("\\", "/")

        # self.uimap = None
        self.currentPage = None
        self.currentPageView = None

        self.uiXmlDoc = None

        self.action_timeout = action_timeout
        self.action_retry_interval = action_retry_interval

