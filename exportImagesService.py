# encoding: utf-8

import gvsig
from org.gvsig.export.spi import ExportService
from org.gvsig.export import ExportLocator
from org.gvsig.tools import ToolsLocator
from org.gvsig.fmap.dal import DALLocator
from org.gvsig.fmap.mapcontext import MapContextLocator
from java.io import File
from java.util import ArrayList

from gvsig import commonsdialog
from gvsig import currentView
from gvsig import openStore
from addons.ExportImages.libexportimage.processExportImage import processExportImage

import os

class ExportImagesService(ExportService):
  def __init__(self, factory, parameters):
    ExportService.__init__(self)
    self.params = parameters
    self._factory = factory
    self.listeners = set()
    self._attributeNamesTranslator = None
    self._requestCancel = False
    self._taskStatus = ToolsLocator.getTaskStatusManager().createDefaultSimpleTaskStatus("ExportImages")
    #range -> set value -> terminate/abort or cancel segun finalice
    
  def getTaskStatus(self):
    return self._taskStatus
  
  def isCancellationRequested(self):
    return self._requestCancel
    
  def cancelRequest(self):
    self._requestCancel = True
    
  def getFactory(self):
    return self._factory
    
  def getParameters(self):
    return self.params
    
  def addFinishListener(self, listener):
    self.listeners.add(listener)
    
  def getAttributeNamesTranslator(self):
        if self._attributeNamesTranslator == None:
          self._attributeNamesTranslator = ExportLocator.getServiceManager().createAttributeNamesTranslator()
        return self._attributeNamesTranslator
  def getTargetOpenStoreParameters(self): # return List<OpenDataStoreParameters> 
    # lista de parameters que se usan para abrir los ficheros que se han creado
    return self._openStores
    
  def export(self, featureSet):
    # Export images process
    field = self.getParameters().getImageField()
    formatName = self.getParameters().getImageFormat()
    outparams = self.getParameters().getImageOutputOption()
    processExportImage(featureSet, field, formatName, outparams, self.taskStatus)
  
    
def main(*args):

    #Remove this lines and add here your code
    sv = ExportImagesService(None, None)
    print "hola mundo"
    pass
