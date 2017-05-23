# -*- coding: cp1252 -*-
'''
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

import re
from robot.api import logger
import time
from selenium import common
from robot.errors import *
from robot.utils import *

class CustomStrategies(object):
    """
    This class contains custom strategies to parse robotframework variables, handle stale elements and frames.
    """

    patternRFVar = re.compile(r'''\${(.*?)}''',
                                            re.UNICODE |
                                            re.VERBOSE |
                                            re.S)

    def _get_read_only_mode_state(self):

        read_only_mode_flag_value = self.builtIn.get_variable_value("${ENABLE_READ_ONLY_MODE}", "NO")

        if read_only_mode_flag_value.upper() == "YES":
            return True
        else:
            return False

    def _parse_rf_variables(self, string):
        """
        Parses the robot framework (RF) variables. Then replaces the variables with values.
        :param string: input string
        :return: parsed string
        """
        logger.debug("Parse function called")
        if self.patternRFVar.search(string):
            # Loop through all matches
            logger.debug("RF Varirable found")
            for item in self.patternRFVar.findall(string):
                # Construct RF Variable
                rfVarName = (("${%s}") % (item))

                # Get RF Variable Value
                rfVarValue = self.builtIn.get_variable_value(rfVarName)

                logger.debug(("Setting variable %s with value %s") % (rfVarName, rfVarValue))

                # Replace RF Variable string with value
                string = string.replace(rfVarName, str(rfVarValue))

        return string

    def _stale_element(self, function, *args):
        """
        Handles all the weird stale element issues. It catches the exception on failure.

        :param function: The selenium function to perform a task.
        :param args: The parameters for the function.
        :return: Looks for invalid/stale element, returns it if found, tries 3 times, then fails. Returns the element
        if found, otherwise return TRUE flag to show that exception has occurred.
        """

        counter = 0

        while counter != 3:
            encounteredException = False
            try:
                func = getattr(self.seleniumlib, '%s' % function)
            except AttributeError:
                raise Exception("Keyword not found: %s" % function)

            logger.info("Running function: %s" % function)

            try:
                result = func(*args)
            except common.exceptions.InvalidElementStateException:
                logger.warn(("Caught InvalidElementStateException for function: %s") % (function))
                self.builtIn.sleep("2s")
                encounteredException = True
            except common.exceptions.StaleElementReferenceException:
                logger.warn(("Caught StaleElementReferenceException for function: %s") % (function))
                self.builtIn.sleep("2s")
                encounteredException = True
            if encounteredException == False:
                counter = 3
            else:
                counter = counter + 1
        return result

    def _wait_for_element(self, locator, modifierAttribute = None):
        """
        Waits for the browser element to appear but looks for staleness prior to that.

        :param locator: The html element locator, e.g. ID, class, xpath, etc.
        :param modifierAttribute: It'll find hidden elements unless specified in the variable not to find it.
        :return: returns the element if found otherwise return true flag to show that exception occurred
        """

        self._stale_element("wait_until_page_contains_element", locator)
        
        if (None if modifierAttribute is None else modifierAttribute.lower()) != "hidden":            
            self._stale_element("wait_until_element_is_visible", locator)

    def _frame_mgt_reselect (self, frame_value):
        """
        Unselect and then select the frame again

        :param locatorValues: frame locators
        """
        #print "FRAMES"
        #print locatorValues
        logger.debug("Selecting frame: %s" % frame_value)
        self.seleniumlib.unselect_frame()
        self._stale_element("wait_until_page_contains_element", frame_value)
        self.seleniumlib.select_frame(frame_value)

    def _frame_dynamic_id(self, frame_value, flow):
        """
        Unselect and then select the frame again

        :param locatorValues: frame locators
        """
        #print "FRAMES"
        #print locatorValues
        logger.debug("Selecting frame: %s" % frame_value)
        dynamic_frame_count = self.builtIn.get_variable_value('${DYNAMIC_FRAME_ID}')

        if dynamic_frame_count is None:
            dynamic_frame_count = 0
            self.builtIn.set_global_variable("${DYNAMIC_FRAME_ID}", dynamic_frame_count)

        logger.debug("Current dynamic frame count: %i" % int(dynamic_frame_count))
        #if flow is not "last":
        #self.builtIn.set_global_variable("${DYNAMIC_FRAME_ID}", dynamic_frame_count)

        dynamic_frame_value = self._parse_rf_variables(frame_value)
        logger.debug("Selecting dynamic frame: %s" % dynamic_frame_value)
        self._frame_mgt_reselect(dynamic_frame_value)

        if flow is "last":
            dynamic_frame_count += 1
            self.builtIn.set_global_variable("${DYNAMIC_FRAME_ID}", dynamic_frame_count)

    def _frame_mgt(self, locatorValues, flow=None):
        """
        Handles the frames within a page. Unselects when not needed, selects and re-selects when needed.
        """
        logger.debug("locatorValues frame: %s" % locatorValues["modifier"])
        logger.debug("locatorValues dynamic_frame: %s" % locatorValues["dynamic_frame"])
        logger.debug("Running flow: %s" % flow)
        if flow == None:
            if locatorValues["modifier"] == "noframe" or locatorValues["modifier"] == "noframe_click_only":
                self.seleniumlib.unselect_frame()
            elif locatorValues["frame"] is not None:
                self._frame_mgt_reselect(locatorValues["frame"])
            #elif locatorValues["dynamic_frame"] is not None:
            #    self._frame_dynamic_id(locatorValues["dynamic_frame"])
            elif self.default_frame != False:
                defaultFrame = self._ui_data(self.default_frame, "frame")
                self._frame_mgt_reselect(defaultFrame["frame"])

        if flow == "page_contains":
            if locatorValues["modifier"] == "noframe_click_only":
                if locatorValues["frame"] is not None:
                    self._frame_mgt_reselect(locatorValues["frame"])
                elif self.default_frame != False:
                    defaultFrame = self._ui_data(self.default_frame, "frame")
                    self._frame_mgt_reselect(defaultFrame["frame"])

            if locatorValues["dynamic_frame"] is not None:
                self._frame_dynamic_id(locatorValues["dynamic_frame"], flow)

        if flow == "last":
            if locatorValues["dynamic_frame"] is not None:
                self._frame_dynamic_id(locatorValues["dynamic_frame"], flow)

    def _ui_data(self, fieldName, validTypes):
        """
        Checks that only one value is returned for requested types.
        Note: This function will be enhanced to deal with more complex UI maps.

        :param fieldName: field names to search for
        :param validTypes: expected field types
        :return: returns only one value for requested types
        """
        
        fieldNames = fieldName.split("|")
        uiList = self.get_data_ui_xml_value(fieldNames[0])
        logger.debug("UIlist: %s" % uiList)
        keyDict = {}
        typeMatchList = []
        typeMatchDict = {}
        pageCheck = None
        frameValue = None
        actionValue = None
        dynamic_frame_value = None
        action_timeout = self.action_timeout
        action_retry_interval = self.action_retry_interval

        for match in uiList:
            if match['type'] in validTypes:
                typeMatchList.append(match['type'])
                typeMatchList.append(match['locator'])

            if match['type'] == "pageCheck":
                pageCheck = match['locator']

            if match['type'] == "frame":
                frameValue = match['locator']

            if match['type'] == "dynamic_frame":
                dynamic_frame_value = match['locator']

            try:
                if match['modifier'] != None:
                    actionValue = match['modifier']
            except KeyError:
                continue

            if match['type'] == 'timeout':
                action_timeout = match['locator']
                if match['modifier'] != None:
                    action_retry_interval = match['modifier']

        if len(typeMatchList) == 0:
            raise Exception ("Invalid type for requested keyword")
        elif len(typeMatchList) > 2:
            raise Exception ("Multiply matches found in : %s" % uiList)
        else:
            logger.debug("typeMatchList Values: %s" % typeMatchList)
            typeMatchDict['type'] = typeMatchList[0]
            typeMatchDict['pageCheck'] = pageCheck
            typeMatchDict['frame'] = frameValue
            typeMatchDict['dynamic_frame'] = dynamic_frame_value
            typeMatchDict['modifier'] = actionValue
            typeMatchDict['action_timeout'] = action_timeout
            typeMatchDict['action_retry_interval'] = action_retry_interval

            # If len is 1 then no additional values have been passed
            if len(fieldNames) == 1:
                typeMatchDict['locator'] = typeMatchList[1]

            # If len is greater than or equal to 2 then additional values have been passed
            if len(fieldNames) >= 2:
                # Remove the xml field name
                del fieldNames[0]

                if len(fieldNames) >= 1:
                    for fieldPair in fieldNames:
                        if "=" in fieldPair:
                            fields = fieldPair.split("=")
                            keyDict[fields[0]] = fields[1]
                
                if self.patternRFVar.search(typeMatchList[1]):
                    locatorText = typeMatchList[1]
                    for item in self.patternRFVar.findall(typeMatchList[1]):
                        try:
                            locatorText = locatorText.replace((("${%s}") % (item)), keyDict[item])
                        except KeyError:
                            raise Exception ("Variable not passed: %s" % item)

                    typeMatchDict['locator'] = locatorText
                else:
                    typeMatchDict['locator'] = (("%s%s") % (typeMatchList[1],fieldNames[0]))

            typeMatchDict["locator"] = self._parse_rf_variables(typeMatchDict["locator"])
            logger.debug("Returning match dict: %s" % typeMatchDict)
            return typeMatchDict

    def internal_wait_until_keyword_succeeds(self, keyword, locator_values, *args):
        """
        Internal keyword to wait until keyword succeeds.

        :param keyword: the keyword to look for
        :param locator_values: the locator values to identify the elements
        :param args: the extra arguments to pass to keyword
        :return: keeps waiting for keyword until timeout
        """
        self.builtIn.wait_until_keyword_succeeds(locator_values['action_timeout'],
                                                 locator_values['action_retry_interval'],
                                                 keyword,
                                                 locator_values,
                                                 *args)
    def __trunc_at(self, s, d="/", n=3):
        """
        Returns s truncated at the n'th (3rd by default) occurrence of the delimiter, d.

        :param s: string to be truncated
        :param d: the delimiter
        :param n: the number of times to use d as delimiter
        :return: the truncated value
        """
        return d.join(s.split(d)[:n])
