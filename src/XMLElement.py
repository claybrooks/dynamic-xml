from lxml import etree as et
import json
        
########################################################################################################################
#                                                                                                                      #
########################################################################################################################
class XMLElement(object):
    
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def __init__(self, specData, xmlElement=None, tag=None):
        self.__subElements = {}

        self.__isMulti = True if (specData['isMulti'] == 'True' or specData['isMulti'] == 'true' or specData['isMulti'] == '1') else False

        self.__xmlElement = xmlElement
        if self.__xmlElement == None:
            self.__xmlElement = et.Element(tag)
        
        self.__specData = specData

        self.__generateFunctionWrappers()
        self.loadFromXml(xmlElement)

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def isMulti(self):
        return self.__isMulti
        
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def getTag(self):
        return self.__xmlElement.tag

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def setText(self, newText):
        self.__xmlElement.text = newText

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def getText(self):
        return self.__xmlElement.text

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
        return self.__xmlElement.attrib

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def getAttribute(self, name):
        if name in self.__xmlElement.attrib.keys():
            return self.__xmlElement.attrib[name]
        else:
            return None

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def hasAttribute(self, name):
        return name in self.__xmlElement.attrib.keys()
    
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def setAttribute(self, name, val):
        stringified = str(val)

        if not self.hasAttribute(name):
            self.__xmlElement.attrib[name] = stringified
        else:
            self.__xmlElement.set(name, stringified)

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def hasElement(self, name):
        return name in self.__subElements.keys()

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def getElement(self, name):
        if self.hasElement(name) and len(self.__subElements[name]) > 0:
            if self.__subElements[name][0].isMulti():
                return self.__subElements[name]
            else:
                return self.__subElements[name][0]

        return None

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def setElement(self, name, obj):
        self.prependElement(name, obj)
        
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
        
        return XMLElement(specData, tag=name)

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
            self.__xmlElement.insert(idx, obj.__xmlElement)

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def removeElement(self, name, idx):
        if not self.hasElement(name):
            return

        del self.__subElements[name][idx]
        self.__xmlElement.remove(idx)

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def appendElement(self, name, obj=None):
        self.addElement(name, -1, obj)
        
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################  
    def prependElement(self, name, obj=None):
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
        self.__xmlElement = xmlElement

        # iterate through all sub elements
        specData = {}
        for element in xmlElement:
            tag = element.tag
            
            if tag not in specData.keys():
                specData[tag] = self.getSubElementSpecData(tag)

            if specData[tag] == None:
                continue

            # build new element
            newEle = XMLElement(specData[tag], xmlElement=element)

            # first time we are seeing this tag
            if tag not in self.__subElements:
                self.__subElements[tag] = []
            
            # append new item
            self.__subElements[tag].append(newEle)

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def __injectWrappingFunction(self, name, prefixName, func, isPlural, *args, **kwargs):

       
        setattr(self, name, func)

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
    def __wrapAttribute(self, name):
        
        # capitalized name
        capitalized =  name.capitalize()

        def get():
            return self.getAttribute(name)

        def has():
            return self.hasAttribute(name)
        
        def _set(newVal):
            return self.setAttribute(name, newVal)

        setattr(self, f'getAttribute{capitalized}', get)
        setattr(self, f'hasAttribute{capitalized}', has)
        setattr(self, f'setAttribute{capitalized}', _set)

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def __wrapElement(self, name):
        
        specData = self.getSubElementSpecData(name)
        if specData == None:
            return

        # whether or not this element can be single or multi
        isMulti= specData['isMulti']
        isMulti = True if (isMulti=='True' or isMulti=='true' or isMulti=='1') else False
            
        # capitalized name
        capitalized =  name.capitalize()

        # plural of the name
        plural = capitalized
        if not name.endswith('s'):
            plural += 's'

        def has():
            return self.hasElement(name)

        def get():
            return self.getElement(name)

        def create():
            return self.createElement(name)

        setattr(self, f'create{capitalized}',                       create)
        setattr(self, f'get{plural if isMulti else capitalized}',   get)
        setattr(self, f'has{plural if isMulti else capitalized}',   has)

        if not isMulti:

            def _set(ele):
                return self.setElement(name, ele)

            setattr(self, f'set{capitalized}', _set)

        else:

            def iterate():
                return self.iterateElement(name)

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
                
            setattr(self, f'add{capitalized}',          add)
            setattr(self, f'remove{capitalized}',       remove)
            setattr(self, f'iterate{plural}',           iterate)
            setattr(self, f'append{capitalized}',       append)
            setattr(self, f'prepend{capitalized}',      prepend)
            setattr(self, f'removeFirst{capitalized}',  removeFirst)
            setattr(self, f'removeLast{capitalized}',   removeLast)
            setattr(self, f'clear{plural}',             clear)
