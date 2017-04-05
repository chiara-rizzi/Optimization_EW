import pickle, sys
import glob, os
import re
import ROOT
from array import array
import json
#import make_table


selections = {"btag60":"bjets_n_60", "btag70":"bjets_n_70", "btag77":"bjets_n_77", "btag85":"bjets_n_85", "5j":"jets_n<=5", "6j":"jets_n<=6", "7j":"jets_n<=7", "anyj":"jets_n<=100",
              "ptj20":"pt_jet_4>20", "ptj30":"pt_jet_4>30", "min_diff":"!_dR", "dR":"!_min_diff", "met_from_180":"!met>150", "met_from_200":"!met>180",
              "ex3b_btag60":"bjets_n_60==3", "ex3b_btag70":"bjets_n_70==3", "ex3b_btag77":"bjets_n_77==3", "ex3b_btag85":"bjets_n_85==3",
              "4b_btag60":"bjets_n_60>=4", "4b_btag70":"bjets_n_70>=4", "4b_btag77":"bjets_n_77>=4", "4b_btag85":"bjets_n_85>=4",
              "met_bins":"met<",
              "met_180_250":"met>180 && met<250",
              "met_250_400":"met>250 && met<400",
              "met_400":"met>400",
              "Zh_mass":"mass_h1_dR>100 && mass_h1_dR<140 && mass_h2_dR>70 && mass_h2_dR<100",
              "hh_mass":"mass_h1_dR>100 && mass_h1_dR<140 && mass_h2_dR>100 && mass_h2_dR<140",
              }
#mysel = ["dR","ptj20","met_from_180","ex3b_btag85"]
mysel = ["btag77"]

name_out="/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/read_results/"+"dict"
#for s in mysel:
#   name_out+="_"
#   name_out+=s
#name_out+=".pickle"

name_out+="_btag77_hhmass_v0.json"

def passes_criteria(elem, signal, sel, string, mysel):
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

def readpickle(inputdir, string, out_name, signal, list_signals, mysel):
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
         #print mysig
         sig_map=dict()
         for key in x.keys():
            if not passes_criteria(x[key], mysig, key, string, mysel):
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
         if passes_criteria(x[key], signal, key, string, mysel):
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
      #print "key"
      #print key
      #print "signal"
      #print signal
      #print 'sel_sig_map[key]'
      #print sel_sig_map[key]
      #print "sel_sig_map[key][0]"
      #print sel_sig_map[key][0]
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

   signal_list=["hh_"+s+"_hh4b" for s in signals]
   signal_list+=["Zh_"+s+"_Zh4b" for s in signals]
   signal_list+=["Zh_"+s+"_ZZ4b" for s in signals]

   print "my signal list!"
   print signal_list

   #sel_dict=dict()
   final_selections=dict()
   final_selections_table=dict()

   str_sel_pickle_300="bjets_n_77*met_180met250*mass_h1_dR_100mass_h1_dR140mass_h2_dR_100mass_h2_dR140"
   str_sel_pickle_500="bjets_n_77*met_250met400*mass_h1_dR_100mass_h1_dR140mass_h2_dR_100mass_h2_dR140"
   str_sel_pickle_800="bjets_n_77*met_400_mass_h1_dR_100mass_h1_dR140mass_h2_dR_100mass_h2_dR140"
   sel_dict_string_300 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_04_03', str_sel_pickle_300, "outpu_not_used.pickle","",signal_list, mysel)
   sel_dict_string_500 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_04_03', str_sel_pickle_500, "outpu_not_used.pickle","",signal_list, mysel)
   sel_dict_string_800 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_04_03', str_sel_pickle_800, "outpu_not_used.pickle","",signal_list, mysel)
   final_selections["hh_300"]=readbigpickle(sel_dict_string_300, "hh_300_hh4b", "")[0]
   final_selections["hh_500"]=readbigpickle(sel_dict_string_500, "hh_500_hh4b", "")[0]
   final_selections["hh_800"]=readbigpickle(sel_dict_string_800, "hh_800_hh4b", "")[0]

   #sel_dict_string = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_test', "dict", "test1.pickle","",["GGM_hh_"+s for s in signals])   
   #print sel_dict_string
   #for s in signals:
      #final_selections["Zh_"+s]=readbigpickle(sel_dict_string, "Zh_"+s+"_Zh4b", "")[0]
      #final_selections["ZZ_"+s]=readbigpickle(sel_dict_string, "Zh_"+s+"_ZZ4b", "")[0]
      #final_selections_table[s]=readbigpickle(sel_dict_string, "GGM_hh_"+s, "")[1]



   print final_selections
   with open(name_out,"w") as outf:
      json.dump(final_selections, outf, indent=2)
   outf.close()
   #pickle.dump(final_selections, open(name_out, "wb" ) )

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


