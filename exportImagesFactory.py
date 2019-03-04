# encoding: utf-8

import gvsig
from org.gvsig.export.spi import AbstractExportServiceFactory
from exportImagesParameters import ExportImagesParameters
from exportImagesService import ExportImagesService

SERVICE_NAME = "ExportImages"

class ExportImagesFactory(AbstractExportServiceFactory):
  def __init__(self):
    AbstractExportServiceFactory.__init__(
      self,
      SERVICE_NAME,
      "_Export Images",
      "_Export_Images"
      )
  def createService(self,parameters):
    return ExportImagesService(self, parameters)
    
  def createParameters(self):
    return ExportImagesParameters()
    
  def hasTabularSupport(self):
        return True
        
  def hasVectorialSupport(self):
        return True
def main(*args):
    egf = ExportImagesFactory()
