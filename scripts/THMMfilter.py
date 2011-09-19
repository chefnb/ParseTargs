import subprocess
import string
import os

# pipe to the TMHMM predictor - hPred = no. of predicted transmembrane helices
  
def isMembraneProtein(seq):
       tmhmm=subprocess.Popen([os.path.join(os.path.abspath("."),'tmhmm-2.0c/bin/tmhmm')],  stdin=subprocess.PIPE, stdout=subprocess.PIPE)

       hpred = int(string.split(string.split(tmhmm.communicate(input=seq)[0])[4],"=")[1])

       return hpred>0 
