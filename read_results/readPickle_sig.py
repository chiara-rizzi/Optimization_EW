import pickle, sys
import glob, os
import re
import ROOT
from array import array
#import make_table


selections = {"btag60":"bjets_n_60", "btag70":"bjets_n_70", "btag77":"bjets_n_77", "btag85":"bjets_n_85", "5j":"jets_n<=5", "6j":"jets_n<=6", "7j":"jets_n<=7", "anyj":"jets_n<=100",
              "ptj20":"pt_jet_4>20", "ptj30":"pt_jet_4>30", "min_diff":"!_dR", "dR":"!_min_diff"}
mysel = ["dR"]

name_out="/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/read_results/"+"dict"
for s in mysel:
   name_out+="_"
   name_out+=s
name_out+=".pickle"

def passes_criteria(elem, signal, sel, string):
   # elem = (significance, nsignal, totbkg, nttbar, error_ttbar, nttbar_raw)
   # * at least 2 signal events (weighted)
   # at least 2 signal events
   #if elem[1][signal] < 2:
      #return False

   # * ttbar rel stat unc < 0.3
   if not elem[3] > 0:
      return False
   if elem[4]/elem[3] > 0.3:
      return False
   for s in mysel:
      if not s in selections:
         print s,"not in selections"
         return False
      if selections[s].startswith("!"):
         if selections[s].replace("!","") in sel:
            return False
      else:
         if not selections[s] in sel:
            return False
   # ttbar > 60%
   #if elem[3]/elem[2] < 0.6:
   #   return False
   
   return True

def readpickle(inputdir, string, out_name, signal, list_signals):
   sel_sig_map=dict()
   print "Intput dir ", inputdir
   os.chdir(inputdir)
   i=0
   for mypickle in glob.glob("*"+string+"*.pickle"):
      print mypickle
      with open(mypickle, 'rb') as handle:   
         x = pickle.load(handle)
      handle.close()
      
      xx = dict()
      for mysig in list_signals:
         #print mysig
         sig_map=dict()
         for key in x.keys():
            if not passes_criteria(x[key], mysig, key, string):
               continue
            sig_map[key]=x[key][0][mysig]         
         isel =0
         for key in sorted(sig_map,key=sig_map.__getitem__, reverse=True):
            if sig_map[key] < 1.79769313486e+308:
               if isel > 0:
                  break         
               xx[key] = x[key]
               #print sig_map[key]
               isel+=1
      if len(list_signals) > 0:
         x = xx

      for key in x.keys():
         #if x[key][0] > 0 and x[key][0] < 1.79769313486e+308:
         key_new=key
         #if "-1" in key:
         #   key_new=key_new.replace("-1", "0")
         if type(x[key][4]) == str:
            print "key"
            print key
            print x[key]
         if passes_criteria(x[key], signal, key, string):
            sel_sig_map[key_new]=x[key]
      i+=1
      #print i,mypickle
      #print "len tot ",len(sel_sig_map),"  len new ",len(x),"\n"
      #print(mypickle)
   #os.chdir('/nfs/pic.es/user/c/crizzi/scratch2/susy_multib/compressed_regions/optimization_code')
   #pickle.dump(sel_sig_map, open( out_name, "wb" ) ) 
   return sel_sig_map

def readbigpickle(sel_sig_map, signal, string):
   #print "\n\nREADING BIG BIG PICKLE!!!\n"
   sig_map = dict()
   for key in sel_sig_map:
      if type(sel_sig_map[key]) == str:
         continue
      #print "key"
      #print key
      #print "signal"
      #print signal
      #print 'sel_sig_map[key]'
      #print sel_sig_map[key]
   #   if passes_criteria(sel_sig_map[key], signal, key):
      #print key
      sig_map[key]=sel_sig_map[key][0][signal]
      
   #pickle.dump(sel_sig_map, open( out_name+"_"+string+"_all_sig.pickle", "wb" ) )

   isel =0
   for key in sorted(sig_map,key=sig_map.__getitem__, reverse=True):
      #if sig_map[key] > 0 and sig_map[key] < 1.79769313486e+308:
      if sig_map[key] < 1.79769313486e+308:
         if isel > 0:
            break
         print "\n\n"
         print signal
         print "BEST SELS:"
         print key
         print "significance for",signal,":",sig_map[key]
         print "signal events:", sel_sig_map[key][1][signal]
         print "total background:",sel_sig_map[key][2]
         print "ttbar:",sel_sig_map[key][3],"pm",sel_sig_map[key][4],"  (rel err:",sel_sig_map[key][4]/sel_sig_map[key][3],")"
         print sel_sig_map[key],"\n"
         isel += 1
   #return (key,key+" && z-ttbar=="+"{:.2f}".format(sel_sig_map[key][3])+" && z-backg=="+"{:.2f}".format(sel_sig_map[key][2])+" && zz-signal=="+"{:.2f}".format(sel_sig_map[key][1][signal])+" && zz-signif=="+"{:.2f}".format(sig_map[key]) +" && z-ttbar-unc=="+"{:.2f}".format(sel_sig_map[key][4]/sel_sig_map[key][3])+" && z-ttbar-frac=="+"{:.2f}".format(sel_sig_map[key][3]/sel_sig_map[key][2])   )
         return (key,key+" && z-ttbar=="+"{:.2f}".format(sel_sig_map[key][3])+" && z-backg=="+"{:.2f}".format(sel_sig_map[key][2])+" && z-signal=="+"{:.2f}".format(sel_sig_map[key][1][signal])+" && z-ttbar-unc=="+"{:.2f}".format(sel_sig_map[key][4]/sel_sig_map[key][3])+" && z-ttbar-frac=="+"{:.2f}".format(sel_sig_map[key][3]/sel_sig_map[key][2])   )
   
   #print "\n\nFINE!!!\n\n"


def printbigpickle(sel_sig_map, signal):
   print "\n\nprint BIG BIG PICKLE!!!\n"
   sig_map = dict()
   for key in sel_sig_map:
      print key
      if key not in sel_sig_map:
         print "not in sel_sig_map!!"
         continue
      #if passes_criteria(sel_sig_map[key], signal):
      sig_map[key]=sel_sig_map[key][0][signal]   
   isel =0
   for key in sorted(sig_map,key=sig_map.__getitem__, reverse=True):
      if isel>0:
         break
      #if sig_map[key] > 0 and sig_map[key] < 1.79769313486e+308:
      if sig_map[key] < 1.79769313486e+308:
         isel+=1
         print "\n\nBEST SELS:"
         print key
         print "significance for",signal,":",sig_map[key]
         print "signal events:", sel_sig_map[key][1][signal]
         print "total background:",sel_sig_map[key][2]
         print "ttbar:",sel_sig_map[key][3],"pm",sel_sig_map[key][4],"  (rel err:",sel_sig_map[key][4]/sel_sig_map[key][3],")"
         #print sel_sig_map[key],"\n"
         print ""
         return key
   
   #print "\n\nFINE!!!\n\n"         

if __name__ == '__main__':

   signals = ["130","150","200","300","400","500","600","800"]

   #sel_dict=dict()
   final_selections=dict()
   final_selections_table=dict()

   sel_dict_string = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle', "dict", "outpu_not_used.pickle","",["GGM_hh_"+s for s in signals])
   #sel_dict_string = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_test', "dict", "test1.pickle","",["GGM_hh_"+s for s in signals])
   for s in signals:
      final_selections[s]=readbigpickle(sel_dict_string, "GGM_hh_"+s, "")[0]
      #final_selections_table[s]=readbigpickle(sel_dict_string, "GGM_hh_"+s, "")[1]

   pickle.dump(final_selections, open(name_out, "wb" ) )

   #for s in signals:
      #printbigpickle(sel_dict_string, s)

   """      
      if final_selections[string]:
         final_selections_table[string]=final_selections_table[string].replace("weight_mc*weight_lumi*weight_btag*weight_elec*weight_muon*weight_jvt*weight_WZ_2_2*","")
      print ""

   print "\n\n\n"

   for key in sorted(final_selections):
      #print key
      #print final_selections[key]
      print ""

   f = open(out_name+".tex","w")
   table2l=""
   if do2L:
      table2l=make_table.make_table(final_selections_table,"2l")   
   table1l=make_table.make_table(final_selections_table,"1l")
   table0l=make_table.make_table(final_selections_table,"0l")   
   intro="\\documentclass[10pt,a4paper,landscape]{article} \n\\usepackage[utf8]{inputenc} \n\\usepackage[english]{babel} \n\\usepackage{amsmath} \n\\usepackage{amsfonts} \n\\usepackage{amssymb} \n\\usepackage{graphicx} \n\\begin{document} \n"
   closure="\\end{document} \n"
   
   f.write(intro)
   f.write(table2l)
   f.write(table1l)
   f.write(table0l)
   f.write(closure)
   f.close()
   """


