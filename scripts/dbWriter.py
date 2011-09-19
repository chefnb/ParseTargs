#
#*****************************************
#
# Sept 2011 - Nick Braun
#
#  DBWriter.py
#
#
#*****************************************
#
# Build  sqlite database from targetsV2.xml (http://targetdb.pdb.org/)
#
# **  Sequence is SOLUBLE if its targetDB status 
# tags include Soluble, Purified, or both 
# 
# ** Sequence is INSOLUBLE if
#    (i)  its targetDB status tags include 'Expressed',
#           but not 'Soluble' or 'Purified'
#    (ii) the record is more than 100 days old
#
# For a discussion of similar criteria, see 
#       Smialowski et al. Bioinformatics v23 p2536 (2007)
#
#******************************************************

import sys
import xml.sax.handler
import xml.sax
import datetime
import time
import sqlite3
import re
import THMMfilter
import os

MAX_PARSE=1e9


class dbWriter():
    def __init__(self,targets_xml,db_filename):

      self.db = sqlite3.connect(os.path.join(os.path.abspath("."),db_filename))
      self.c=self.db.cursor()     

      self.c.execute("create table Meta(records_parsed integer, status text, datestamp text)")
      self.c.execute("insert into Meta values (0, 'building', ?)", (datetime.date.today(),))
    

      self.c.execute('''create table parseTargs
              (tdb_ref text, length integer, de_count integer, isSoluble integer, isTM integer)''')

      parser = xml.sax.make_parser()
      parser.setFeature(xml.sax.handler.feature_external_ges, False)
      parser.setContentHandler(targetDBHandler(self))
      try:
         parser.parse(targets_xml)
      except Terminate, value:

        self.close(str(value))
     
    def updateCount(self,count):
       self.c.execute("update Meta set records_parsed= ?", (count,))
       self.db.commit()


    def write(self,data):

      seq = data['sequence']
      if data['isSoluble']: isSoluble=1
      else: isSoluble=0


      if THMMfilter.isMembraneProtein(seq): isTM=1
      else: isTM =0
     
 
      self.c.execute('insert into parseTargs values (?,?,?,?,?)', 
                          ( data['tdbRef'],
                            len(seq), 
                            len(re.sub('[^DE]+','',seq)), 
                            isSoluble ,
                            isTM
                          ) )

    

    def close(self,status):
   
        self.c.execute("update Meta set status= ?", (status,))   
        self.db.commit()
        self.c.close()
      
    
      

class Terminate(Exception):
     pass

#*************************************************************************************

class targetDBHandler(xml.sax.handler.ContentHandler):
    def __init__(self,dbW):
     
        self.dbWriter = dbW
        self.count=0
        self.today = datetime.date.today()

       
    def output(self,isSoluble):
            
        self.dbWriter.write({'tdbRef': self.id,
                             'sequence':self.sequence,
                             'isSoluble': isSoluble 
                             })
          
    def startElement(self, name,attrs):
        self.buffer = ""
    
        if name == "target":
            self.isExpressed=False
            self.isSoluble=False
     
    def characters(self, content):
        self.buffer += content
 
    
    def endElement(self, name):

        if name == "id": self.id=self.buffer
        if name == "sequence": self.sequence=re.sub(r'\n','',self.buffer).strip()
        if name == "date": 
            self.date=self.buffer
            try:
                ed=time.strptime(self.date,"%Y-%m-%d")
                entrydate=datetime.date(ed.tm_year,ed.tm_mon,ed.tm_mday)
                self.elapsedTime =  (self.today-entrydate).days
            except:
                self.elapsedTime = 0

        if name == "target":
            self.count+=1
         
            if (not self.isSoluble) and self.isExpressed: 
               if self.elapsedTime > 100 :  self.output(False)
            if self.isSoluble: self.output(True)

            self.dbWriter.updateCount(self.count)
   
            if self.count==MAX_PARSE:
              raise Terminate("stopped (incomplete)")
           

        if name== "status":
            if self.buffer.strip() == 'Expressed':
                self.isExpressed = True
            if self.buffer.strip() == 'Soluble':
                self.isSoluble = True
            if self.buffer.strip() == 'Purified':
                self.isSoluble = True
      
       
    def endDocument(self):
        
        raise Terminate("complete")
        

