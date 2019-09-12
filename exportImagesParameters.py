# encoding: utf-8

import gvsig
from org.gvsig.tools.util import HasAFile
from org.gvsig.export.spi import AbstractExportParametersGeometry

class ExportImagesParameters(AbstractExportParametersGeometry, HasAFile):
  def __init__(self, factory):
    AbstractExportParametersGeometry.__init__(self, factory)
    self.folderFile  = None #file
    self.imageField = None
    self.imageFormat = None
    self.imageOutputOption = None
  def needsSelectTargetProjection(self):
    return False # para que saque el panel de proyeccion
    
  def getServiceName(self):
    pass
    
  def getImageField(self):
    return self.imageField
    
  def setImageField(self, imageField):
    self.imageField = imageField
    
  def getImageFormat(self):
    return self.imageFormat
    
  def setImageFormat(self, imageFormat):
    self.imageFormat = imageFormat
    
  def getImageOutputOption(self):
    return self.imageOutputOption
    
  def setImageOutputOption(self, imageOutputOption):
    self.imageOutputOption = imageOutputOption
 
def main(*args):

    #Remove this lines and add here your code

    print "hola mundo"
    params = ExportImagesParameters()
    print dir(params)
    pass
