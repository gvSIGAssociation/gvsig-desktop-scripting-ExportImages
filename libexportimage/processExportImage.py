# encoding: utf-8

import gvsig
from org.gvsig.tools.swing.api import ToolsSwingLocator
from javax.imageio import ImageIO
from java.io import File
import os, sys
from gvsig import logger
from gvsig import LOGGER_WARN,LOGGER_INFO,LOGGER_ERROR
from org.gvsig.tools.dispose import DisposeUtils

def getUniqueValueFileByField(name, path, formatName):
  filename = str(name)+"."+formatName.lower()
  newpath =  os.path.join(path,filename)
  f = File(newpath)
  i = 0
  while f.exists():
    nid = str(name)+str(i)+"."+formatName.lower()
    f = File(os.path.join(path,nid))
    i+=1
  print f
  return f
  
def processExportImage(store, field, outputPath, formatName, nameFromField=None, nameFromExp=None):
  if not formatName in ["PNG", "JPEG", "GIF"]:
    logger("Not valid format for export images", LOGGER_ERROR)
    return
  sm = ToolsSwingLocator.getToolsSwingManager()
  si = sm.createSimpleImage()

  try:
    fset = store.getFeatureSet() # Filter from export tool or selection
    for f in fset:
      # Get image
      value = f.get(field)
      if value==None or value=="":
        continue
      si.set(value)
      im = si.getBufferedImage()
      if im==None:
        logger("Not able to get Bufferded Image from field "+field+" value:"+value, LOGGER_ERROR)
      # Save image
      if nameFromField!=None:
        name = f.get(nameFromField)
        if name == None or name=="": continue
        output = getUniqueValueFileByField(name, outputPath, formatName)
      else:
        #output = getUniqueValueFileByExp()
        pass
      ImageIO.write(im, formatName, output)
  except:
    ex = str(sys.exc_info()[1])
    logger("Not able to export: "+ex, LOGGER_ERROR)
    try:
      DisposeUtils.disposeQuietly(fset)
    except:
      logger("Not able dispose export images feature set", LOGGER_ERROR)
      
def main(*args):
  store = gvsig.currentLayer().getFeatureStore()
  field = "resblob"
  format = "PNG" #https://docs.oracle.com/javase/tutorial/2d/images/saveimage.html
  outputPath = "/home/osc/Working/exportimages/"
  nameFromField = "id"
  nameFromExp = None
  processExportImage(store, field, outputPath, format, nameFromField, nameFromExp)
