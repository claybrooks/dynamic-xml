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

        self.__subElementClasses = {}
        
        self.__specData = specData
        self.__generateFunctionWrappers()

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
    def subElements(self, key=None):
        
        if key == None:
            return self.__subElements
        else:
            if self.hasElement(key):
                return self.__subElements[key]
            else:
                return []

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def attributes(self):
        return self.__attributes

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def getAttribute(self, name):
        if name in self.__attributes:
            return self.__attributes[name]
        else:
            return None

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def hasAttribute(self, name):
        return name in self.__attributes
    
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def setAttribute(self, name, val):
        if name not in self.__attributes:
            self.__attributes[name] = XMLAttribute(name)

        return self.__attributes[name].setValue(val)

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def hasElement(self, name):
        return name in self.__subElements.keys()

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def getElement(self, name):
        if self.hasElement(name):
            return self.__subElements[name]
        else:
            return None

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def iterateElement(self, name):
        return self.subElements(name)

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def createElement(self, name):
        specData = self.getSubElementSpecData(name)
        if specData == None:
            return None
        
        return XMLElement(None, specData)

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def addElement(self, name, idx, obj=None):
        if not self.hasElement(name):
            self.__subElements[name] = []

        if obj == None:
            obj = self.createElement(name)

        if obj != None:
            self.__subElements[name].insert(idx, obj)
            
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def removeElement(self, name, idx):
        if not self.hasElement(name):
            return

        del self.__subElements[name][idx]

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def appendElement(self, name, obj=None):
        self.addElement(name, -1, obj)
        
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################  
    def prependElement(self, name, XMLElement=None):
        self.addElement(name, 0, obj)

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def removeFirstElement(self, name):
        self.removeElement(name, 0)

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def removeLastElement(self, name):
        self.removeElement(name, -1)

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def clearElements(self, name):
        if self.hasElement(name):
            self.__subElements[name] = []

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def getSubElementSpecData(self, eleName):
        if eleName in self.__specData['subElements']:
            try:
                with open(self.__specData['subElements'][eleName], 'r') as f:
                    return json.load(f)
            except Exception as e:
                return None

        return None

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
            self.__attributes[key] = XMLAttribute(key)
            self.__attributes[key].setValue(value)

        specData = {}
        # iterate through all sub elements
        for element in xmlElement:
            tag = element.tag
            
            if tag not in specData.keys():
                specData[tag] = self.getSubElementSpecData(tag)

            if specData[tag] == None:
                continue

            # build new element
            newEle = XMLElement(element, specData[tag])

            # first time we are seeing this tag
            if tag not in self.__subElements:
                self.__subElements[tag] = list()
            
            # append new item
            self.__subElements[tag].append(newEle)

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
            return self.getAttribute(attrName)

        def has():
            return self.hasAttribute(attrName)
        
        def _set(newVal):
            return self.setAttribute(attrName, newVal)

        capitalized = attrName.capitalize()

        setattr(self, f'getAttribute{capitalized}', get)
        setattr(self, f'hasAttribute{capitalized}', has)
        setattr(self, f'setAttribute{capitalized}', _set)

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def __wrapElement(self, name):
        
        # we've already created this class
        def has():
            return self.hasElement(name)

        def get():
            return self.getElement(name)

        isMulti = self.__specData['isMulti']

        capitalized = name.capitalize()

        if not isMulti:
            setattr(self, f'get{capitalized}', get)
            setattr(self, f'has{capitalized}', has)
        else:

            plural = capitalized
            if not capitalized.endswith('s'):
                plural += 's'

            def iter():
                return self.iterateElement(name)

            def create():
                return self.createElement(name)

            def add(idx, obj=None):
                self.addElement(name, idx, obj)

            def remove(idx, obj=None):
                self.removeElement(name, idx)

            def append(obj=None):
                self.appendElement(name,obj)
                
            def prepend(obj=None):
                self.prependElement(name, obj)

            def removeFirst():
                self.removeFirstElement(name)

            def removeLast():
                self.removeLastElement(name)

            def clear():
                self.clearElements(name)
                
            setattr(self, f'create{capitalized}',       create)
            setattr(self, f'add{capitalized}',          add)
            setattr(self, f'remove{capitalized}',       remove)
            setattr(self, f'get{plural}',               get)
            setattr(self, f'has{plural}',               has)
            setattr(self, f'iter{plural}',              iter)
            setattr(self, f'append{capitalized}',       append)
            setattr(self, f'prepend{capitalized}',      prepend)
            setattr(self, f'removeFirst{capitalized}',  removeFirst)
            setattr(self, f'removeLast{capitalized}',   removeLast)
            setattr(self, f'clear{plural}',             clear)