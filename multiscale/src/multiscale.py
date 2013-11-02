# Basic imports
import os 
import sys 
import logging 
import debug 

logger = logging.getLogger('multiscale')
from lxml import etree

import sqlite3 as sql 
import re

class Multiscale :
  
  def __init__(self, xmlDict) :
    self.xmlDict = xmlDict 
    self.dbdir = 'db'
    self.dbname = 'models.db'
    self.dbpath = os.path.join(self.dbdir, self.dbname)
    self.includedFiles = list()

    if not os.path.exists(self.dbpath) :
      try :
        os.makedirs(self.dbdir)
      except Exception as e :
        debug.printDebug("ERROR"
            , "Faild to create directory {0} with error {1}".format(self.dbdir, e))
        sys.exit(0)
    #self.conn = sql.connect(self.dbpath)
    self.conn = sql.connect(":memory:")
    self.cursor = self.conn.cursor()
    debug.printDebug("INFO", "Object of class Multiscale intialized ...")

  def isTag(self, tagName, nmElem) :
    if re.search(r'^\{(?P<namesapce>[^}^{]+)\}'+tagName+'\s*$', nmElem.tag) :
      return True
    else :
      return False
  def parseAndValidateWithSchema(modelName, modelPath) :
      
      prefixPath = ''
      if modelName == 'xml' :
        schemaPath = os.path.join(prefixPath, 'moose_xml/moose.xsd')

      try :
        schemaH = open(schemaPath, "r")
        schemaText = schemaH.read()
        schemaH.close()
      except Exception as e :
        debug.printDebug("WARN", "Error reading schema for validation."+
          " Falling back to validation-disabled parser."
          + " Failed with error {0}".format(e))
        return parseWithoutValidation(modelName, modelPath)
      # Now we have the schema text 
      schema = etree.XMLSchema(etree.XML(schemaText))
      xmlParser = etree.XMLParser(schema=schema, remove_comments=True)
      with open(modelPath, "r") as xmlTextFile :
          return etree.parse(xmlTextFile, xmlParser)

  def parseWithoutValidation(modelName, modelPath) :
      xmlParser = etree.XMLParser(remove_comments=True)
      try :
        xmlRootElem = etree.parse(modelPath, xmlParser)
      except Exception as e :
        debug.printDebug("ERROR", "Parsing failed. {0}".format(e))
        return 
      return xmlRootElem 

  def segmentToQuery(self, segXML) :
      values = dict()
      for k in segXML.keys() :
        values[k] = segXML.get(k)
      # get parent, distal and proximal.
      for elem in segXML :
        if self.isTag('parent', elem) :
          values['parent'] = elem.get('segment')
          if elem.get('fractionAlong') :
            values['fractionAlong'] =  elem.get('fractionAlong')
        elif self.isTag('proximal', elem) :
          for k in elem.keys() :
            values["proximal_"+k.strip()] = elem.get(k)
        elif self.isTag('distal', elem) :
          for k in elem.keys() :
            values["distal_"+k.strip()] = elem.get(k)
      # build query
      query = "INSERT OR REPLACE INTO topology ("
      query += ",".join(values.keys())
      query += ') VALUES (' + ", ".join(["'"+v.strip()+"'" for v in values.values()]) + ')'
      return query
  def segmentToQuery(self, segXML) :
      values = dict()
      for k in segXML.keys() :
        values[k] = segXML.get(k)
      # get parent, distal and proximal.
      for elem in segXML :
        if self.isTag('parent', elem) :
          values['parent'] = elem.get('segment')
          if elem.get('fractionAlong') :
            values['fractionAlong'] =  elem.get('fractionAlong')
        elif self.isTag('proximal', elem) :
          for k in elem.keys() :
            values["proximal_"+k.strip()] = elem.get(k)
        elif self.isTag('distal', elem) :
          for k in elem.keys() :
            values["distal_"+k.strip()] = elem.get(k)
      # build query
      query = "INSERT OR REPLACE INTO topology ("
      query += ",".join(values.keys())
      query += ') VALUES (' + ", ".join(["'"+v.strip()+"'" for v in values.values()]) + ')'
      return query
  def insertSegmentGroupsIntoDB(self, segGrpXML) :
      groupId = segGrpXML.get('id')
      for k in segGrpXML :
        query = "UPDATE OR REPLACE topology SET "
        query += "segment_group='"+groupId+"' WHERE id='" + k.get('segment') + "'"
        self.executeQuery(query)

        if 'include' in k.keys() : 
          debug.printDebug("WARN", "Element include is not implemented")
        if 'path' in k.keys() : 
          debug.printDebug("WARN", "Element path is not implemented")
        if 'subTree' in k.keys() :
          debug.printDebug("WARN", "Element subTree is not implemented")
        if 'inhomogeneousParam' in k.keys() : 
          debug.printDebug("WARN", "Element inhomogeneousParam is not implemented")

  def insertSegmentGroupsIntoDB(self, segGrpXML) :
      groupId = segGrpXML.get('id')
      for k in segGrpXML :
        query = "UPDATE OR REPLACE topology SET "
        query += "segment_group='"+groupId+"' WHERE id='" + k.get('segment') + "'"
        self.executeQuery(query)

        if 'include' in k.keys() : 
          debug.printDebug("WARN", "Element include is not implemented")
        if 'path' in k.keys() : 
          debug.printDebug("WARN", "Element path is not implemented")
        if 'subTree' in k.keys() :
          debug.printDebug("WARN", "Element subTree is not implemented")
        if 'inhomogeneousParam' in k.keys() : 
          debug.printDebug("WARN", "Element inhomogeneousParam is not implemented")

  def insertBioPhysicalPropertiesIntoDB(self, elemXML) :
      for c in elemXML.getchildren() :
        if self.isTag('membraneProperties', c) :
          for prop in c :
            print prop
        elif self.isTag('intracellularProperties', c) :
          print "Intracellular properties"
        elif self.isTag('extracellularProperties', c) :
          print "Extracellular properties"
        else :
          debug.printDebug("WARN", "Unimplemented element {0}".format(c))

  def insertBioPhysicalPropertiesIntoDB(self, elemXML) :
      for c in elemXML.getchildren() :
        if self.isTag('membraneProperties', c) :
          for prop in c :
            print prop
        elif self.isTag('intracellularProperties', c) :
          print "Intracellular properties"
        elif self.isTag('extracellularProperties', c) :
          print "Extracellular properties"
        else :
          debug.printDebug("WARN", "Unimplemented element {0}".format(c))


  def extractTransformLoad(self, modelType, xmlRootNode) :
    if modelType == 'nml' :
      self.etlNMLModel(xmlRootNode)
    else :
        pass 

  def etlNMLModel(self, nmlTree) :
    debug.printDebug("STEP", "ETLing a nml model")
    nmlRootNode = nmlTree.getroot()
    for c in  [ child  for child in nmlRootNode if type(child.tag) == str] :
      if self.isTag('include', c) :
        self.includedFiles.append(c.get('href'))
      elif self.isTag('cell', c) :
        self.insertCellIntoDB(c)
      else :
        debug.printDebug("WARN", "{0} is not implemented yet.".format(child.tag))
   
  # Function to insert a cell into database 
  def insertCellIntoDB(self, cell) :
    for c in cell.iterchildren(tag=etree.Element) :
      if self.isTag('morphology', c) :
        for elem in c.iterchildren(tag=etree.Element) :
          if self.isTag('segment', elem) :
             segmentDict = dict()
             self.executeQuery(self.segmentToQuery(elem))
          elif self.isTag('segmentGroup', elem) :
             self.insertSegmentGroupsIntoDB(elem)
          else :
            debug.printDebug("INFO" , "This element {0} is not supported".format(elem))
      elif self.isTag('biophysicalProperties', c) :
         self.insertBioPhysicalPropertiesIntoDB(c)
      else :
        debug.printDebug("WARN", "{0} not implemented".format(c.tag))

  def segmentToQuery(self, segXML) :
      values = dict()
      for k in segXML.keys() :
        values[k] = segXML.get(k)
      # get parent, distal and proximal.
      for elem in segXML :
        if self.isTag('parent', elem) :
          values['parent'] = elem.get('segment')
          if elem.get('fractionAlong') :
            values['fractionAlong'] =  elem.get('fractionAlong')
        elif self.isTag('proximal', elem) :
          for k in elem.keys() :
            values["proximal_"+k.strip()] = elem.get(k)
        elif self.isTag('distal', elem) :
          for k in elem.keys() :
            values["distal_"+k.strip()] = elem.get(k)
      # build query
      query = "INSERT OR REPLACE INTO topology ("
      query += ",".join(values.keys())
      query += ') VALUES (' + ", ".join(["'"+v.strip()+"'" for v in values.values()]) + ')'
      return query
  def segmentToQuery(self, segXML) :
      values = dict()
      for k in segXML.keys() :
        values[k] = segXML.get(k)
      # get parent, distal and proximal.
      for elem in segXML :
        if self.isTag('parent', elem) :
          values['parent'] = elem.get('segment')
          if elem.get('fractionAlong') :
            values['fractionAlong'] =  elem.get('fractionAlong')
        elif self.isTag('proximal', elem) :
          for k in elem.keys() :
            values["proximal_"+k.strip()] = elem.get(k)
        elif self.isTag('distal', elem) :
          for k in elem.keys() :
            values["distal_"+k.strip()] = elem.get(k)
      # build query
      query = "INSERT OR REPLACE INTO topology ("
      query += ",".join(values.keys())
      query += ') VALUES (' + ", ".join(["'"+v.strip()+"'" for v in values.values()]) + ')'
      return query
  def insertSegmentGroupsIntoDB(self, segGrpXML) :
      groupId = segGrpXML.get('id')
      for k in segGrpXML :
        query = "UPDATE OR REPLACE topology SET "
        query += "segment_group='"+groupId+"' WHERE id='" + k.get('segment') + "'"
        self.executeQuery(query)

        if 'include' in k.keys() : 
          debug.printDebug("WARN", "Element include is not implemented")
        if 'path' in k.keys() : 
          debug.printDebug("WARN", "Element path is not implemented")
        if 'subTree' in k.keys() :
          debug.printDebug("WARN", "Element subTree is not implemented")
        if 'inhomogeneousParam' in k.keys() : 
          debug.printDebug("WARN", "Element inhomogeneousParam is not implemented")

  def insertSegmentGroupsIntoDB(self, segGrpXML) :
      groupId = segGrpXML.get('id')
      for k in segGrpXML :
        query = "UPDATE OR REPLACE topology SET "
        query += "segment_group='"+groupId+"' WHERE id='" + k.get('segment') + "'"
        self.executeQuery(query)

        if 'include' in k.keys() : 
          debug.printDebug("WARN", "Element include is not implemented")
        if 'path' in k.keys() : 
          debug.printDebug("WARN", "Element path is not implemented")
        if 'subTree' in k.keys() :
          debug.printDebug("WARN", "Element subTree is not implemented")
        if 'inhomogeneousParam' in k.keys() : 
          debug.printDebug("WARN", "Element inhomogeneousParam is not implemented")

  def insertBioPhysicalPropertiesIntoDB(self, elemXML) :
      for c in elemXML.getchildren() :
        if self.isTag('membraneProperties', c) :
          for prop in c :
            print prop
        elif self.isTag('intracellularProperties', c) :
          print "Intracellular properties"
        elif self.isTag('extracellularProperties', c) :
          print "Extracellular properties"
        else :
          debug.printDebug("WARN", "Unimplemented element {0}".format(c))

  def insertBioPhysicalPropertiesIntoDB(self, elemXML) :
      for c in elemXML.getchildren() :
        if self.isTag('membraneProperties', c) :
          for prop in c :
            print prop
        elif self.isTag('intracellularProperties', c) :
          print "Intracellular properties"
        elif self.isTag('extracellularProperties', c) :
          print "Extracellular properties"
        else :
          debug.printDebug("WARN", "Unimplemented element {0}".format(c))


  def initDB(self, dropOldTables = False) :
    query = '''CREATE TABLE IF NOT EXISTS topology
      (id INTEGER PRIMARY KEY ASC
      , name VARCHAR
      , parent INTEGER 
      , fractionAlong REAL default '0.0'
      , proximal_x REAL
      , proximal_y REAL 
      , proximal_z REAL
      , proximal_diameter REAL
      , distal_x REAL
      , distal_y REAL
      , distal_z REAL
      , distal_diameter REAL
      , x REAL 
      , y REAL  
      , z REAL 
      , segment_group VARCHAR
      , remark TEXT
      )'''
    self.executeQuery(query)
   
    query = '''CREATE TABLE IF NOT EXISTS electrical
      (type VARCHAR PRIMARY KEY -- Type of cell
      , leakReversal REAL       -- leakReversal potential
      , threshold REAL          -- Threshold voltage
      , reset REAL
      , tau REAL
      , refract REAL
      , capacitance REAL
      , leakConductance REAL
      , a REAL                  -- Izhikenvich Cell model
      , b REAL                  -- Izhikenvich cell model
      , c REAL                  -- Izhikenvich cell model 
      , d REAL                  -- Izhikenvich cell model
      , gL REAL
      , EL REAL
      , VT REAL
      , delT REAL
      , tauw REAL
      , Idel REAL
      , Idur REAL
      )'''
    self.executeQuery(query)

    query = '''CREATE TABLE IF NOT EXISTS mapping
      (id INTEGER
      , seg_from INTEGER, fromType VARCHAR
      , seg_to INTEGER,  toType VARCHAR
      , lhsVar VARCHAR
      , rhsExpr VARCHAR 
      , comment TEXT
      , PRIMARY KEY (seg_from, seg_to, lhsVar)
      )'''
    self.executeQuery(query)

    query = '''CREATE TABLE IF NOT EXISTS property
      (segment_group VARCHAR    -- Group of segment
      , p_name VARCHAR            -- Name of property 
      , p_type VARCHAR            -- type of property 
      , p_value REAL              -- Value of property 
      , p_unit  VARCHAR           -- Unit of property
      , comment TEXT              -- Optional comment 
      )'''
    self.executeQuery(query)


  def executeQuery(self, query) :
    with self.conn :
      try :
        self.cursor.execute(query)
      except Exception as e :
        debug.printDebug("ERR", "Failed to execute query with error {0}".format(e))
        print("+ Query was: {0}".format(query))
 

  # This is the entry point of this class.
  def buildMultiscaleModel(self) :
      debug.printDebug("INFO", "Starting to build multiscale model")   
      self.initDB()
      for xml in self.xmlDict :
        xmlRootNodeList = self.xmlDict[xml]
        for xmlRootNode in xmlRootNodeList :
          self.extractTransformLoad(xml, xmlRootNode)


  
  def exit(self) :
    # Clean up before you leave
    self.cursor.commit()
    self.conn.close()
    sys.exit()

  # Write down the tests, whenever needed.
  




