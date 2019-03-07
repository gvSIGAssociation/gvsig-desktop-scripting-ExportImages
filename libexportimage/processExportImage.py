# encoding: utf-8

import gvsig
from org.gvsig.tools.swing.api import ToolsSwingLocator
from javax.imageio import ImageIO
from java.io import File
import os, sys
from gvsig import logger
from gvsig import LOGGER_WARN,LOGGER_INFO,LOGGER_ERROR
from org.gvsig.tools.dispose import DisposeUtils
from org.gvsig.fmap.dal.feature import FeatureAttributeDescriptor
from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator
from org.gvsig.fmap.dal import DALLocator

def getUniqueValueFileByField(name, path, formatName):
  filename = str(name)+"."+formatName.lower()
  newpath =  os.path.join(path,filename)
  f = File(newpath)
  i = 0
  while f.exists():
    nid = str(name)+str(i)+"."+formatName.lower()
    f = File(os.path.join(path,nid))
    i+=1
  return f
  
def processExportImage(featureSet, field, formatName, outparams, taskStatus=None):
  if not formatName in ["PNG", "JPEG", "GIF"]:
    logger("Not valid format for export images", LOGGER_ERROR)
    return
  sm = ToolsSwingLocator.getToolsSwingManager()
  si = sm.createSimpleImage()
  if taskStatus!=None:
   taskStatus.setRangeOfValues(0, featureSet.getSize())
  if isinstance(field, FeatureAttributeDescriptor):
    field = field.getName()
  try:
    ooption = outparams["option"]
    oparams = outparams["params"]
    n = 0
    if ooption==1:
      for f in featureSet:
        if taskStatus!=None:
          n+=1
          taskStatus.setCurValue(n)
          if taskStatus.isCancellationRequested():
            return
        value = f.get(field)
        if value==None or value=="":
          continue
        si.set(value)
        im = si.getBufferedImage()
        if im==None:
          logger("Not able to get Bufferded Image from field "+str(field)+" value:"+str(value), LOGGER_ERROR)
          continue
        # Save image
        ofield = oparams["field"]
        if isinstance(ofield, FeatureAttributeDescriptor):
          ofield = ofield.getName()
        output =  f.get(ofield)
        ImageIO.write(im, formatName, output)
    elif ooption==2:
      for f in featureSet:
        if taskStatus!=None:
          n+=1
          taskStatus.setCurValue(n)
          if taskStatus.isCancellationRequested():
            return
        value = f.get(field)
        if value==None or value=="":
          continue
        si.set(value)
        im = si.getBufferedImage()
        if im==None:
          logger("Not able to get Bufferded Image from field "+str(field)+" value:"+str(value), LOGGER_ERROR)
          continue
        ofield = oparams["field"]
        if isinstance(ofield, FeatureAttributeDescriptor):
          ofield = ofield.getName()
        oname = f.get(ofield)
        if oname == None or oname=="": continue
        outputPath = oparams["path"].getAbsolutePath()
        output = getUniqueValueFileByField(oname, outputPath, formatName)
        ImageIO.write(im, formatName, output)
    elif ooption==3:
        s =  ExpressionEvaluatorLocator.getManager().createSymbolTable()
        fst = DALLocator.getDataManager().createFeatureSymbolTable()
        s.addSymbolTable(fst)
        exp = oparams["expression"]
        if exp.isEmpty():
          logger("Expression is empty", LOGGER_ERROR)
          return
        for f in featureSet:
          if taskStatus!=None:
            n+=1
            taskStatus.setCurValue(n)
            if taskStatus.isCancellationRequested():
              return
          value = f.get(field)
          if value==None or value=="":
            continue
          si.set(value)
          im = si.getBufferedImage()
          fst.setFeature(f)
          output = exp.execute(s)
          outputex = output + "." +formatName.lower()
          if os.path.exists(outputex):
            logger("Already exists: "+ outputex, LOGGER_ERROR)
            continue
          ImageIO.write(im, formatName, File(outputex))
      
  except:
    ex = str(sys.exc_info()[1])
    logger("Not able to export: "+ex+ " caused on: " + ex.__class__.__name__, LOGGER_ERROR)
    try:
      DisposeUtils.disposeQuietly(featureSet)
    except:
      logger("Not able dispose export images feature set", LOGGER_ERROR)
      
def main(*args):
  fset = gvsig.currentLayer().getFeatureStore().getFeatureSet()
  field = "resblob"
  formatName = "PNG" #https://docs.oracle.com/javase/tutorial/2d/images/saveimage.html
  ft = gvsig.currentLayer().getFeatureStore().getDefaultFeatureType().getAttributeDescriptor("id")
  outparams = {"option":2,"params":{"path":File("/home/osc/Working/exportimages/"), "field":ft}}
  exp = ExpressionEvaluatorLocator.getManager().createExpression()
  exp.setPhrase("CONCAT('/home/osc/Working/exportimages/', id)")
  outparams = {"option":3,"params":{"expression":exp}}
  processExportImage(fset, field, formatName, outparams)