
from lxml import etree as et

from XMLElement import XMLElement
import json

########################################################################################################################
#                                                                                                                      #
########################################################################################################################
class XMLFile(object):

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def __init__(self, fullPathToXml, fullPathToXmlSpec):
        self.__xmlRoot              = None
        self.__fullPathToXml        = fullPathToXml
        self.__fullPathToXmlSpec    = fullPathToXmlSpec

        try:
            with open(fullPathToXmlSpec, 'r') as f:
                self.__specData = json.load(f)
        except Exception as e:
            print (e)
            return

        self.loadFromFile(fullPathToXml)

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def loadFromFile(self, fullPath):
        try:
            with open(fullPath, 'r') as f:
                self.__xmlData = et.parse(f)
        except Exception as e:
            print (e)
            return

        if self.__xmlData.getroot() == None:
            return

        self.__root = XMLElement(self.__specData, xmlElement=self.__xmlData.getroot())

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def saveToFile(self, fullPath='', *args, **kwargs):
        pathToUse = self.__fullPathToXml
        if fullPath != '':
            pathToUse = fullPath

        self.__xmlData.write(file=pathToUse, pretty_print=True, *args, **kwargs)

    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    def getRoot(self):
        return self.__root

########################################################################################################################
#                                                                                                                      #
########################################################################################################################
if __name__=='__main__':
    xml = XMLFile('TestFiles/Test.xml', 'TestFiles/Root.json')
    root = xml.getRoot()

    for test in root.iterTests():
        if test.hasAttributeAttr():
            print (test.getAttributeAttr())

        if test.hasAttributeAttr2():
            print (test.getAttributeAttr2())

        if not test.hasResults():
            newResult = test.createResult()
            newResult.setText('Hello, new result!')
            newResult.setAttributeTestattr('Set dynamically')
            test.appendResult(newResult)

        for result in test.iterResults():
            if result.hasAttributeTestattr():
                print (result.getAttributeTestattr())

                result.setAttributeTestattr("Updating to a new value!")
                print (result.getAttributeTestattr())

    xml.saveToFile(fullPath='TestFiles/ModifiedInput.xml')