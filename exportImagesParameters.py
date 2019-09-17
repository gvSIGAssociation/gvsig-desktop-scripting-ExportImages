# encoding: utf-8

import gvsig
from org.gvsig.tools.util import HasAFile
from org.gvsig.export.spi import AbstractExportParametersGeometry

class ExportImagesParameters(AbstractExportParametersGeometry, HasAFile):
  def __init__(self, factory):
    AbstractExportParametersGeometry.__init__(self, factory)
    self.factoryName = factory.getName()
    self.folderFile  = None #file
    self.imageField = None
    self.imageFormat = None
    self.imageOutputOption = None
    
  def needsSelectTargetProjection(self):
    return False # para que saque el panel de proyeccion
    
  def getServiceName(self):
    return self.factoryName
    
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

  def clone(self):
    print "ExportImagesParameters trying to clone"
    clone = AbstractExportParametersGeometry.clone(self)
    print "clone: ", clone
    print ".. done clone and return"
    return clone
    
def main(*args):

    #Remove this lines and add here your code

    print "hola mundo"
    params = ExportImagesParameters(None)
    print dir(params)
    pass
