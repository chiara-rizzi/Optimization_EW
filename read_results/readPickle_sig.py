import pickle, sys
import glob, os
import re
import ROOT
from array import array
import json
import argparse
#import make_table

def passes_criteria(elem, signal, sel, string, mysel, tt_frac, Z_frac, tt_Z_frac, stat_unc):
   # elem = (significance, nsignal, totbkg, nttbar, error_ttbar, nttbar_raw, error_bkg)

   if not elem[2]>0.4:
      return False
   
   if elem[6]/elem[2] > stat_unc:
      return False

   if tt_Z_frac>0:
      if not (elem[3]["ttbar"]+elem[3]["Zjets"])>0:
         return False
      if (elem[3]["ttbar"])+elem[3]["Zjets"]/elem[2] < tt_Z_frac:
         return False

   if tt_frac>0:
      if not (elem[3]["ttbar"])>0:
         return False
      if (elem[3]["ttbar"]/elem[2]) < tt_frac:
         return False

   if Z_frac>0:
      if not (elem[3]["Zjets"])>0:
         return False
      if (elem[3]["Zjets"]/elem[2]) < Z_frac:
         return False
   
   for s in mysel:
      if not s in selections:
         #print s,"not in selections"
         return False
      if s.startswith("!"):
         if s.replace("!","") in sel:
            #print "no sel"
            return False
      else:
         if not s in sel:
            #print "no sel"
            return False

   return True

def readpickle(inputdir, string, out_name, signal, list_signals, mysel, tt_frac, Z_frac, tt_Z_frac, stat_unc):
   sel_sig_map=dict()
   print "Intput dir ", inputdir
   os.chdir(inputdir)
   i=0
   for mypickle in glob.glob("*"+string+"*.pickle"):
      print "---> reading",i
      print mypickle
      with open(mypickle, 'rb') as handle:   
         x = pickle.load(handle)
      handle.close()
      
      xx = dict()
      for mysig in list_signals:
         #print "mysig"
         #print mysig
         sig_map=dict()
         for key in x.keys():
            #for elem in x[key]:
            #   print elem
            #print key
            if not passes_criteria(x[key], mysig, key, string, mysel, tt_frac, Z_frac, tt_Z_frac, stat_unc):
               #print "not passed"
               continue
            #print "PASSES"
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
         if passes_criteria(x[key], signal, key, string, mysel, tt_frac, Z_frac, tt_Z_frac, stat_unc):
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
   #print sel_sig_map
   for key in sel_sig_map:
      if type(sel_sig_map[key]) == str:
         continue
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
         print "total background:",sel_sig_map[key][2],"pm",sel_sig_map[key][6],"  (rel err:",sel_sig_map[key][6]/sel_sig_map[key][2],")"
         if sel_sig_map[key][3]["ttbar"]>0:
            print "ttbar:",sel_sig_map[key][3]["ttbar"],"pm",sel_sig_map[key][4]["ttbar"],"  (rel err:",sel_sig_map[key][4]["ttbar"]/sel_sig_map[key][3]["ttbar"],")"
            print "ttbar percentage:",(sel_sig_map[key][3]["ttbar"]/sel_sig_map[key][2])*100,"%"
         #print sel_sig_map[key],"\n"
         isel += 1
         return (key,key)
   
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
         print "ttbar:",sel_sig_map[key][3]["ttbar"],"pm",sel_sig_map[key][4]["ttbar"],"  (rel err:",sel_sig_map[key][4]["ttbar"]/sel_sig_map[key][3]["ttbar"],")"
         #print sel_sig_map[key],"\n"
         print ""
         return key
   
   #print "\n\nFINE!!!\n\n"         

if __name__ == '__main__':

   ROOT.gROOT.SetBatch(ROOT.kTRUE)
   
   parser = argparse.ArgumentParser()

   parser.add_argument('--suff_out', default='_hh4b_test', type=str, help='Suffix for the output json file')
   parser.add_argument('--masses', default=["200","300","500","600","800","900"],nargs='+', help='masses')
   parser.add_argument('--pref_sig', default='GGM_hh_', type=str, help='Signal prefix (part before the mass)')
   parser.add_argument('--suff_sig', default='_hh4b', type=str, help='Signal sufix (part after the mass)')
   parser.add_argument('--sel_name', default='*17_09_03*', type=str, help='String to file in the *name* of the json file')
   parser.add_argument('--sel', default=[], nargs='+', help='List of requirements to find in the selection')
   parser.add_argument('--folder', default='/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_09_03', type=str, help='Folder with pickle files inside')
   parser.add_argument('--tt_frac', default=0., type=float, help='Require ttbar fraction higher than this' )
   parser.add_argument('--Z_frac', default=0., type=float, help='Require Z fraction higher than this' )
   parser.add_argument('--tt_plus_Z_frac', default=0., type=float, help='Require ttbar plus Z+Jets fraction higher than this' )
   parser.add_argument('--max_stat_unc', default=0.4, type=float, help='Maximum value allowed of total statistical uncertainty' )

   args = parser.parse_args()

   name_out="/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/read_results/"+"dict"
   name_out+=args.suff_out+".json"

   final_selections=dict()

   signals = args.masses
   signal_list=[]
   signal_list+=[args.pref_sig+m+args.suff_sig for m in args.masses]

   print "my signal list!"
   print signal_list

   first_round=readpickle(args.folder, args.sel_name, "outpu_not_used.pickle","",signal_list, args.sel, args.tt_frac, args.Z_frac, args.tt_plus_Z_frac, args.max_stat_unc) 

   for m in args.masses:
      final_selections["SR"+args.suff_sig+"_"+m]=readbigpickle(first_round, args.pref_sig+m+args.suff_sig, "")[0]

   print ""
   print ""
   print ""
   print final_selections
   with open(name_out,"w") as outf:
      json.dump(final_selections, outf, indent=2)
   outf.close()


