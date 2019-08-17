from lxml import etree as et
import json

from XMLAttribute import XMLAttribute

########################################################################################################################
#                                                                                                                      #
########################################################################################################################
class XMLElement(object):
    
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def __init__(self, xmlElement, specData):
        self.__subElements = {}
        self.__attributes = {}
        self.__text = ""
        self.__tag = ""
        self.__specData = specData

        self.loadFromXml(xmlElement)

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def getTag(self):
        return self.__tag

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def setText(self, newText):
        self.__text = newText

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def getText(self):
        return self.__text

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def getSubElements(self):
        return self.__subElements

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def getAttributes(self):
        return self.__attributes

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def loadFromXml(self, xmlElement):

        # bad data
        if xmlElement == None:
            return

        # save off tag
        self.__tag = xmlElement.tag

        # save off text data
        self.__text = xmlElement.text

        # iterate through all attributes
        for key, value in xmlElement.items():
            self.__attributes[key] = XMLAttribute(key, value)

        specData = {}

        # iterate through all sub elements
        for element in xmlElement:
            tag = element.tag

            if tag not in specData:
                try:
                    with open(self.__specData['subElements'][tag], 'r') as f:
                        specData[tag] = json.load(f)
                except Exception as e:
                    print (e)
                    return

            # build new element
            newEle = XMLElement(element, specData[tag])

            # first time we are seeing this tag
            if tag not in self.__subElements:
                self.__subElements[tag] = list()
            
            # append new item
            self.__subElements[tag].append(newEle)

        self.__generateFunctionWrappers()

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def __generateFunctionWrappers(self):

        # go through attributes
        for key in self.__specData['attributes']:
            self.__wrapAttribute(key)

        # go through elements
        for key in self.__specData['subElements'].keys():
            self.__wrapElement(key)

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def __wrapAttribute(self, attrName):

        def get():
            if attrName in self.__attributes:
                return self.__attributes[attrName]
            else:
                return None

        def has():
            return attrName in self.__attributes
        
        def _set(newVal):
            if attrName not in self.__attributes:
                return False

            return self.__attributes[attrName].setValue(newVal)

        capitalized = attrName.capitalize()

        setattr(self, f'getAttribute{capitalized}', get)
        setattr(self, f'hasAttribute{capitalized}', has)
        setattr(self, f'setAttribute{capitalized}', _set)

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def __wrapElement(self, eleName):

        def has():
            return eleName in self.__subElements

        def get():
            if has():
                return self.__subElements[eleName]
            else:
                return None

        capitalized = eleName.capitalize()
        setattr(self, f'getElement{capitalized}', get)
        setattr(self, f'hasElement{capitalized}', has)

