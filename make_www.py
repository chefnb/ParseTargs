#
# update site in www directory
#

import os
import sqlite3
import re
import shutil


shutil.copyfile('workspace/parseTargs.db', 'www/parseTargs.db')
shutil.copyfile('workspace/barchart_data.js', 'www/barchart_data.js')

c = sqlite3.connect('workspace/parseTargs.db').cursor()  

template = open('index_template.html')
gadget = template.read().format(** 
        {'summary':  open('workspace/summary.html').read(),
         'datestamp': c.execute("select datestamp from Meta").fetchone()[0],
          'total_parsed': c.execute("select records_parsed from Meta").fetchone()[0],
          'download_size':  os.path.getsize('workspace/parseTargs.db')/1e6
         })

#open("workspace/gadget.xml","w").write(re.sub(r'\n','',gadget).strip())
open("www/index.html","w").write(gadget)


