# encoding: utf-8

import gvsig
from org.gvsig.export.spi import AbstractExportServiceFactory
from exportImagesParameters import ExportImagesParameters
from exportImagesService import ExportImagesService



class ExportImagesFactory(AbstractExportServiceFactory):
  SERVICE_NAME = "ExportImages"
  def __init__(self):
    AbstractExportServiceFactory.__init__(
      self,
      self.SERVICE_NAME,
      "_Export_Images_from_field",
      "_Export_Images_from_field"
      )
  def createService(self,parameters):
    return ExportImagesService(self, parameters)
    
  def createParameters(self):
    return ExportImagesParameters(self)
    
  def hasTabularSupport(self):
    return True
        
  def hasVectorialSupport(self):
    return True
    
def main(*args):
    egf = ExportImagesFactory()
    egf.createParameters()
