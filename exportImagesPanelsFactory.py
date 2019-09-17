# encoding: utf-8

import gvsig
from org.gvsig.export.swing.spi import AbstractExportPanelsFactory
from exportImagesFactory import ExportImagesFactory
from exportImagesPanels import ExportImagesPanels

class ExportImagesPanelsFactory(AbstractExportPanelsFactory):
  def __init__(self):
    AbstractExportPanelsFactory.__init__(self, ExportImagesFactory.SERVICE_NAME)

  def createPanels(self, processPanel, exportParameters):
    return ExportImagesPanels(self, processPanel, exportParameters)

def main(*args):

    #Remove this lines and add here your code

    print "hola mundo"
    pass
