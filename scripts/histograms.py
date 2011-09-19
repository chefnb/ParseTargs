#
#*****************************************
#
#  tdb_histograms.py  
#
#  Sept 2011 - Nick Braun
#
#  generate json file for barchart presentation of targetDB data via Google visualization API
#
#  4 charts: 
#    length vs frequency     (membrane/non-membrane)
#    DE content vs frequency  (" " )
# 
# 
#
# NB data in the pickle files is formatted as [length,DE content, TM(yes/no) ]
#
#
#*****************************************

import os
import math
import pickle
import pprint
import random
import sys
import sqlite3


def bar(dbCursor, LvsDE, isSoluble, isTM, theMin,theMax):

  #return dbCursor.execute("select count(*) from TDBdataset where ?>? and ?<? and isSoluble=? and isTM=?", (LvsDE,theMin,LvsDE,thieMax,isSoluble,isTM)).fetchone()[0]
  
 
  return dbCursor.execute("select count(*) from parseTargs where {0}>{1} and {2}<{3} and isSoluble={4} and isTM={5}".format(LvsDE,theMin,LvsDE,theMax,isSoluble,isTM)).fetchone()[0]
  
  

def histo(dbCursor, LvsDE, isTM , histo_max,histo_step):

    blocks_lower=range(0,histo_max,histo_step)
    blocks_upper=range(histo_step,histo_max+histo_step,histo_step)
    histo=[]

    for lower in blocks_lower:
    
       upper=blocks_upper[blocks_lower.index(lower)]
       histo.append({
                   'label': "{0}-{1}".format(lower,upper),
                   's':   bar(dbCursor,LvsDE,1,isTM,lower,upper),
                   'i':   bar(dbCursor,LvsDE,0,isTM,lower,upper)
       })
         
    return histo


#************************************************************************

def histograms(db_filename):

  c = sqlite3.connect(db_filename).cursor()

  length_g_histograms=[]
  length_m_histograms=[]
  for binsize in [10,20,50,100,200]:
    length_g_histograms.append({"binsize": binsize, "bar": histo(c,'length',0,1000,binsize)})
    length_m_histograms.append({"binsize": binsize, "bar": histo(c,'length',1,1000,binsize)})

  de_g_histograms=[]
  de_m_histograms=[]
  for binsize in [2,5,10,20,50]:
    de_g_histograms.append({"binsize": binsize, "bar": histo(c,'de_count',0,100,binsize)})
    de_m_histograms.append({"binsize": binsize, "bar": histo(c,'de_count',1,100,binsize)})


  json_out="var data= {0}".format({
               'length_g':length_g_histograms,
               'length_m': length_m_histograms,
               'de_g': de_g_histograms,
               'de_m': de_m_histograms
               })

  open("workspace/barchart_data.js","w").write(json_out)
  open("js/barchart_data.js","w").write(json_out)


  

