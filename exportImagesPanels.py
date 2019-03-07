# encoding: utf-8

import gvsig
from gvsig.libs.formpanel import FormPanel
from gvsig import logger
from gvsig import LOGGER_WARN,LOGGER_INFO,LOGGER_ERROR

import os

from org.gvsig.fmap.dal.swing.expressionevaluator import FeatureStoreElement
from org.gvsig.app.project.documents.view import ViewDocument
from org.gvsig.app.project.documents.table import TableDocument
from org.gvsig.export.swing.spi import AbstractExportPanels
from org.gvsig.export.swing import ExportSwingLocator
#from org.gvsig.export.swing.spi import ExportPanelsManager
from org.gvsig.export.swing.spi import ExportPanel
from org.gvsig.export.dbf.swing.panels import EncodingPanel
from org.gvsig.tools.swing.api import ToolsSwingLocator
from org.gvsig.andami import Utilities
from org.gvsig.app import ApplicationLocator
from org.gvsig.fmap.dal.swing import DALSwingLocator
from org.gvsig.expressionevaluator.swing import ExpressionEvaluatorSwingLocator
from org.gvsig.fmap.dal.swing import DataSwingManager
from org.gvsig.fmap.dal import DALLocator

from javax.swing import ButtonGroup
from java.io import File
from javax.swing.filechooser import FileFilter
from javax.swing import DefaultComboBoxModel


from exportImagesParameters import ExportImagesParameters

class MyFileFilter(FileFilter):
   def accept(self, f):
     return (f.isDirectory())
   def getDescription(self):
     return None
     
class ExportImagesPanels(AbstractExportPanels):
  def __init__(self, factory, processPanel, parameters):
    AbstractExportPanels.__init__(self, factory, processPanel, parameters)
    self.initPanels()
  
  def initPanels(self):
        manager = ExportSwingLocator.getExportPanelsManager()
        
        #self.add(EncodingPanel(
        #        self.getProcessPanel(), 
        #        self.getParameters()
        #    )
        #)
        self.add(ImagesPanelOptions(
                 self.getProcessPanel(),
                 self.getParameters()
             )
        )

class ImagesPanelOptions(FormPanel, ExportPanel):
  def __init__(self, processPanel, parameters):
    ExportPanel.__init__(self)
    FormPanel.__init__(self, gvsig.getResource(__file__,"exportImagesPanels.xml"))
    # hay un picker para folder
    self.pickerFolder = None
    self.processPanel = processPanel
    self.params = parameters
    self.store = gvsig.currentLayer().getFeatureStore()
    self.initComponents()
  def btnTest_click(self,*args):
    self.nextPanel()
  def initComponents(self):
    dialogTitle = "_Select_folder"
    fileChooserID = "idPathGMLSelector"
    seticon = True
    # Init
    ## Button group
    self.btgOptions = ButtonGroup()
    self.btgOptions.add(self.rdbOption1)
    self.btgOptions.add(self.rdbOption2)
    self.btgOptions.add(self.rdbOption3)
    ## Image format
    self.cmbImageFormat.addItem("PNG")
    self.cmbImageFormat.addItem("JPEG")
    self.cmbImageFormat.addItem("GIF")
    ## Pickers
    ### Field with image data
    swm = DALSwingLocator.getSwingManager()
    self.pickerFieldsImageData = swm.createAttributeDescriptorPickerController(self.cmbImageField)
    self.pickerFieldsPath = swm.createAttributeDescriptorPickerController(self.cmbPathField)
    self.pickerFieldsName = swm.createAttributeDescriptorPickerController(self.cmbPathFieldName)
    self.pickerFolder = ToolsSwingLocator.getToolsSwingManager().createFolderPickerController(
       self.txtPath,
       self.btnPath)
    
    eesmanager = ExpressionEvaluatorSwingLocator.getManager()
    self.pickerExp = eesmanager.createExpressionPickerController(self.txtExp, self.btnExp)

    self.pickerExpStore= swm.createFeatureStoreElement(self.pickerExp)
    self.pickerExp.addElement(self.pickerExpStore)
    # Input
    ## Layer
    allDocuments = self.getAllValidDocuments()
    if len(allDocuments)==0:
      logger("Not able to find 2 tables to execute the tool", LOGGER_INFO)
      return
    else:
      self._updateAllUI()

  def _updateAllUI(self):

    # Input params dependant of layer
    swm = DALSwingLocator.getSwingManager()
    ## Field with image data
    ft1 = self.store.getDefaultFeatureType()
    self.pickerFieldsImageData.setFeatureType(ft1)
    
    # Output params
    ## Use absolute path from ield
    self.pickerFieldsPath.setFeatureType(ft1)
    ## Export to folder using name
    self.pickerFieldsName.setFeatureType(ft1)
    ## Expression for absolute path
    self.pickerExpStore.setFeatureStore(self.store)
    ### Preview expression
    ## Sample feature
    sampleFeature = None
    try:
      sampleFeature = store.getFeatureSelection().first()
      if sampleFeature == None:
        sampleFeature = store.first()
    except:
      logger("Not able to create Sample Feature for FieldCalculatorTool", LOGGER_WARN)
    
    if sampleFeature!=None:
      dataManager = DALLocator.getDataManager()
      featureSymbolTable = dataManager.createFeatureSymbolTable()
      featureSymbolTable.setFeature(sampleFeature)
      self.pickerExp.setPreviewSymbolTable(featureSymbolTable.createParent())

  def getIdPanel(self):
    return "ExportImagesPanelOptions"
  def getTitlePanel(self):
    pass
  def validatePanel(self):
    return True
  def enterPanel(self):
    initialPath = File(Utilities.TEMPDIRECTORYPATH)
    self.pickerFolder.set(initialPath)
    self.pickerFolder.setFileFilter(MyFileFilter())
    self._updateAllUI()
    
  def previousPanel(self):
    pass
  def nextPanel(self):
    #recoger valores del formulario y guardarlos en parameters
    self.params.setImageField(self.pickerFieldsImageData.get())
    self.params.setImageFormat(self.cmbImageFormat.getSelectedItem())
    if self.rdbOption1.isSelected():
      outparams={"option":1,"params":{"path",self.pickerFieldsPath.get()}} #DefaultFeatureAttributeDescriptor
    elif self.rdbOption2.isSelected():
      outparams={"option":2,"params":{"field":self.pickerFieldsName.get(),"path":self.pickerFolder.get()}}
    elif self.rdbOption3.isSelected():
      outparams={"option":3,"params":{"expression":self.pickerExp.get()}}
    else:
      pass
    self.params.setImageOutputOption(outparams)
    print "params:", self.params.getImageOutputOption()

  def getAllValidDocuments(self):
    application = ApplicationLocator.getManager()
    project = application.getCurrentProject()
    views = project.getDocuments()
    all = []
    for view in views:
      #print view, type(view)
      if isinstance(view, ViewDocument):
          #print view, type(view)
          for layer in view.getMapContext().getLayers():
            #print "--", layer==mlayer, layer.getName()
            all.append(layer)
      elif isinstance(view, TableDocument):
        #print "--", view
        all.append(view)
    return all
    
def main(*args):

    g = ImagesPanelOptions(None, ExportImagesParameters())
    g.showTool("")
    g.asJComponent()
    g.nextPanel()
