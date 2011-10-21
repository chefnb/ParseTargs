
# extend ParseTargs with further indices (i.e., in addition to length and DE)
# currently: turn_forming residues NGPS

import sqlite3
import re


out_db = sqlite3.connect("workspace/pT2.db")
c=out_db.cursor()     
    
c.execute('''create table parseTargs
              (tdb_ref text, length integer, de_count integer, turn_forming integer, isSoluble integer, isTM integer)''')
     

seqStream= sqlite3.connect('workspace/TargsSeq.db').cursor().execute("select tdb_ref,sequence, isSoluble, isTM from parseTargs")

while True:

 seq=seqStream.fetchone()
 
 c.execute('insert into parseTargs values (?,?,?,?,?,?)', 
                          ( seq[0],
                            len(seq[1]), 
                            len(re.sub('[^DE]+','',seq[1])), 
                            len(re.sub('[^NGPS]+','',seq[1])), 
                            seq[2] ,
                            seq[3]
                          ) )
 out_db.commit()

