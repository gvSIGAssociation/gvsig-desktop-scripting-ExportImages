# encoding: utf-8

import gvsig
from gvsig import uselib
uselib.use_plugin("org.gvsig.exportto.app.mainplugin")

from exportImagesPanelsFactory import ExportImagesPanelsFactory
from exportImagesFactory import ExportImagesFactory

from org.gvsig.export.swing import ExportSwingLibrary
from org.gvsig.export.swing import ExportSwingLocator
from org.gvsig.tools.library import AbstractLibrary
from org.gvsig.export import ExportLibrary
from org.gvsig.export import ExportLocator
    
class ExportImagesLibrary(AbstractLibrary):
  def __init__(self, *args):
      self.doRegistration()
      self.doPostInitialize()
      
  def doRegistration(self):
    self.super__registerAsServiceOf(ExportSwingLibrary)
    self.super__registerAsServiceOf(ExportLibrary)
  
  def doInitialize(self): 
    pass
    
  def doPostInitialize(self):
    manager = ExportLocator.getServiceManager()
    swingManager = ExportSwingLocator.getExportPanelsManager()
    
    manager.register(ExportImagesFactory())
    swingManager.register(ExportImagesPanelsFactory())

def main(*args):
    ExportImagesLibrary()