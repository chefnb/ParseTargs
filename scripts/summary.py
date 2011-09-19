#*****************************************
#
# tdb_summary.py  
#
#
# Sept 2011 - Nick Braun
#
#
#*****************************************


import math
import pprint
import sqlite3
import os


def build_record(X_Y):
 
 try:  
  xm = sum( [x for x,y in X_Y] )/len(X_Y) # mean
  xm2 = sum( [x*x for x,y in X_Y] )/len(X_Y) # second moment
  xsd=math.sqrt(xm2-xm*xm)       # standard deviation

  ym = sum( [y for x,y in X_Y] )/len(X_Y)
  ym2 = sum( [y*y for x,y in X_Y] )/len(X_Y)
  ysd=math.sqrt(ym2-ym*ym)
  
  r= sum( [ (x-xm)*(y-ym) for x,y in X_Y ] )/xsd/ysd/len(X_Y)

  return {              'total': len(X_Y),
                        'Pearson_coeff': r,
                        'length': { 'mean':  xm, 'sd': xsd }, 
                        'de':     { 'mean':  ym, 'sd': ysd }
             }

 except:
  return {              'total': 0,
                        'Pearson_coeff': 0,
                        'length': { 'mean':  0, 'sd': 0 }, 
                        'de':     { 'mean':  0, 'sd': 0 }
             }


def summary(db_filename):

  db = sqlite3.connect(db_filename)        
  dbCursor = db.cursor()           

  cytoplasmic_s= dbCursor.execute("select length, de_count from parseTargs where isSoluble=1 and isTM=0").fetchall()
  cytoplasmic_i= dbCursor.execute("select length, de_count from parseTargs where isSoluble=0 and isTM=0").fetchall()
  membrane_s= dbCursor.execute("select length, de_count from parseTargs where isSoluble=1 and isTM=1").fetchall()
  membrane_i= dbCursor.execute("select length, de_count from parseTargs where isSoluble=0 and isTM=1").fetchall()

  html_summary = open("html/summary_html.template").read().format(** {
            'cytoplasmic': {'soluble': build_record(cytoplasmic_s), 'insoluble': build_record(cytoplasmic_i)},
            'membrane': {'soluble': build_record(membrane_s), 'insoluble': build_record(membrane_i)}  
           })

  open("workspace/summary.html","w").write(html_summary)

  return html_summary
  




