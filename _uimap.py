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

import os
from robot.api import logger
import xml.etree.ElementTree as ET


class UiMap(object):

    def set_ui_map(self, uiXmlFile):

        self.currentPage = None
        self.currentPageView = None

        xmlFilePath = os.path.join(self.resource_dir, uiXmlFile).replace("\\", "/")

        self.seleniumlib._info("UI Map XML doc: %s" % xmlFilePath)

        self.uiXmlDoc = ET.parse(xmlFilePath)

    def change_page_view(self, newPageView):
        """ This will allow you to change the XML search path without having to execute a click action keyword.

        If more then one xml path is passed, i.e path/path, then a new base search path will be set.

        Example, simple page view change.
        | Change Page View | `Some Page` |

        Example, page view change that will update the base page search path.
        | Change Page View | `New Parent / Some Page` |

        Example, page view change that will change base page search path.
        | Change Page View | `/ New Parent ` |

        """
        pages = newPageView.split("/")
        numberOfNewPages = len(pages)

        logger.debug("Starting current page: %s" % self.currentPage)
        logger.debug("Starting current page view: %s" % self.currentPageView)
        logger.debug("Passed new page view value: %s" % newPageView)

        if newPageView.startswith("/"):
            logger.debug("A new base page has been passed")
            self.currentPage = newPageView
            self.currentPageView = None

        elif numberOfNewPages == 1:
            logger.debug("Only a new page view has been passed")
            self.currentPageView = newPageView

        elif numberOfNewPages > 1:
            logger.debug("A new page view & additional base page has been passed")
            self.currentPageView = pages[numberOfNewPages-1]
            pages.pop()
            newBasePage = "/".join(pages)
            self.currentPage += "/"
            self.currentPage += newBasePage

        logger.debug("Updated current page: %s" % self.currentPage)
        logger.debug("Updated current page view: %s" % self.currentPageView)



    def get_data_ui_xml_value(self, xmlName):
        """ This is normally used internally to other keywords, however can be used to obtain a value from the UI XML map.

        XML searching is conducted in the following order:
            Firstly looks at XML path based on RF variable ${currentPage} OR ${currentPageView}.
            Secondly looks at XML path based on RF variable ${currentPage} AND pass Page View.
            Thridly looks at XML commonMappings.

        """

        # Sets the name and value of the xmlName that will be searched for.
        #nameAttribute = (("[@name='%s']") % (xmlName))
        nameAttribute = (("%s") % (xmlName))

        # Firstly search for matching elements in the current page view
        #xmlPath = ((".%s/%s/uiMapping%s") % (self.currentPage, self.currentPageView, nameAttribute))
        xmlPath = ((".%s/%s/%s") % (self.currentPage, self.currentPageView, nameAttribute))

        matches = self._parse_ui_xml_values(xmlPath)

        # If no matches, then search in the current page level
        if len(matches) == 0:
            #xmlPath = ((".%s/uiMapping%s") % (self.currentPage, nameAttribute))
            xmlPath = ((".%s/%s") % (self.currentPage, nameAttribute))
            matches = self._parse_ui_xml_values(xmlPath)

        # If no matches, then search in commmonMappings under page view node
        if len(matches) == 0:
            #xmlPath = (("./commonMappings/%s/uiMapping%s") % (self.currentPageView, nameAttribute))
            xmlPath = (("./commonMappings/%s/%s") % (self.currentPageView, nameAttribute))
            matches = self._parse_ui_xml_values(xmlPath)

        # If no matches, then search in just commonMappings
        if len(matches) == 0:
            #xmlPath = (("./commonMappings/uiMapping%s") % (nameAttribute))
            xmlPath = (("./commonMappings/%s") % (nameAttribute))
            matches = self._parse_ui_xml_values(xmlPath)

        # If no matches were found, then raise an exception
        if len(matches) == 0:
            raise Exception ("No match found for: %s" % xmlName)
        else:
            return matches

    def _parse_ui_xml_values(self, xmlXPath):
        """
        This function will findall matches for the passed XPath.
        It will return a list containing matched name, type and locator (XML Text).
        If nothing is found, then an empty list is returned.
        """
        tmp_list =[]
        logger.debug("Using xml XPath: %s" % xmlXPath)

        # Does the xml request to get the elements text back
        for item in self.uiXmlDoc.findall(xmlXPath):
            tmp_dict = {}
            tmp_dict['type'] = item.get('type')
            tmp_dict['modifier'] = item.get('modifier')
            tmp_dict['locator'] = item.text
            tmp_list.append(tmp_dict)

        return tmp_list

