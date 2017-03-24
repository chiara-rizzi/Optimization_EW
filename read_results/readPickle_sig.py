import pickle, sys
import glob, os
import re
import ROOT
from array import array
import make_table

#my_type="2Lonly_impose_mtbmin_MJSumAtHighMeffv2_mT2L_high_mass_sig_low_met_ov_meff_noTTstatLimit"

doTest1=False
doTest2=False
doTest3=False
doTest4=False
doTest5=False
doTest6=False
doTest7=False
doTest8=False
doTest9=False
doTest10=False
doTest11=False
doTest12=False
doTest13=False
doTest14=False

my_type="01_10_test14" 
doTest14=True

#test1
# mT 150
# mtbmin 120
# MET 350
# no MET/meff
# pT4th > 30
# MJSum > 150
# bjets >= 3

doMeff4jForGbb=False

do2L=False

out_name="SR_35ifb_"+my_type
if do2L:
   out_name+="_2L"

def is_low_meff(string):
   string_list=string.split("_")
   index_meff=string_list.index("meff")
   meff_min=string_list[index_meff+2]
   if float(meff_min)<1000:
      return True
   else:
      return False

def is_high_meff(string):
   string_list=string.split("_")
   index_meff=string_list.index("meff")
   meff_min=string_list[index_meff+2]
   if float(meff_min)>1999:
      return True
   else:
      return False
   
def is_gbb(sel):
   if not "(signal_leptons_n)==0" in sel:
      return False
   if not "jets_n>=4 && jets_n<=6" in sel:
      return False
   return True

def passes_criteria(elem, signal, sel, string):
   # elem = (significance, nsignal, totbkg, nttbar, error_ttbar, nttbar_raw)
   # * at least 2 signal events (weighted)
   # at least 2 signal events
   #if elem[1][signal] < 2:
      #return False

   # * ttbar rel stat unc < 0.3
   if not elem[3] > 0:
      return False
   #if elem[4]/elem[3] > 0.3 and not "0l_9_j_meff_incl_2400" in string and not "1l_8_j_meff_incl_1800_2400" in string:
   #if elem[4]/elem[3] > 0.3:
   #   return False
   #if elem[4]/elem[3] > 0.4:
   #   return False


   if doTest14:
      if not "met/meff_incl>=-1" in sel:
         return False
      if not "mTb_min>140" in sel:
         return False
      if not "met>300" in sel:
         return False
      if not is_gbb(sel) and not is_low_meff(string):
         if is_high_meff(string):
            if not "MJSum_rc_r08pt10>200" in sel: 
               return False
         else:
            if not "MJSum_rc_r08pt10>150" in sel: 
               return False
      else:
         if not "MJSum_rc_r08pt10>-1" in sel:
            return False
      if not "bjets_n>=3" in sel:
         return False
      if not "pt_jet_4>30" in sel and not is_gbb(sel):
         return False
      if "(signal_leptons_n)==0" in sel:
         if not "mT>=-1" in sel:
            return False
      else:
         if not "mT>=150" in sel:
            return False


   if doTest13:
      if not "met/meff_incl>=-1" in sel:
         return False
      if not "mTb_min>100" in sel:
         return False
      if not "met>300" in sel:
         return False
      if not is_gbb(sel) and not is_low_meff(string):
         if not "MJSum_rc_r08pt10>150" in sel: 
            return False
      else:
         if not "MJSum_rc_r08pt10>-1" in sel:
            return False
      if not "bjets_n>=3" in sel:
         return False
      if not "pt_jet_4>30" in sel and not is_gbb(sel):
         return False
      if "(signal_leptons_n)==0" in sel:
         if not "mT>=-1" in sel:
            return False
      else:
         if not "mT>=150" in sel:
            return False


   if doTest12:
      if not "met/meff_incl>=-1" in sel:
         return False
      if not "mTb_min>120" in sel:
         return False
      if not "met>300" in sel:
         return False
      if not is_gbb(sel) and not is_low_meff(string):
         if not "MJSum_rc_r08pt10>150" in sel: 
            return False
      else:
         if not "MJSum_rc_r08pt10>-1" in sel:
            return False
      if not "bjets_n>=3" in sel:
         return False
      if not "pt_jet_4>30" in sel and not is_gbb(sel):
         return False
      if "(signal_leptons_n)==0" in sel:
         if not "mT>=-1" in sel:
            return False
      else:
         if not "mT>=150" in sel:
            return False


   if doTest11:
      if not "met/meff_incl>=-1" in sel:
         return False
      if not "mTb_min>120" in sel:
         return False
      #if not "met>350" in sel:
      #   return False
      if not is_gbb(sel) and not is_low_meff(string):
         if "MJSum_rc_r08pt10>-1" in sel: 
            return False
      #else:
      #   if not "MJSum_rc_r08pt10>-1" in sel:
      #      return False
      if not "bjets_n>=3" in sel and not is_gbb(sel):
         return False
      #if not "pt_jet_4>30" in sel and not is_gbb(sel):
      #   return False
      if "(signal_leptons_n)==0" in sel:
         if not "mT>=-1" in sel:
            return False
      else:
         if not "mT>=150" in sel:
            return False


   if doTest10:
      if not "met/meff_incl>=-1" in sel:
         return False
      if not "mTb_min>120" in sel:
         return False
      #if not "met>350" in sel:
      #   return False
      if not is_gbb(sel) and not is_low_meff(string):
         if "MJSum_rc_r08pt10>-1" in sel: 
            return False
      #else:
      #   if not "MJSum_rc_r08pt10>-1" in sel:
      #      return False
      if not "bjets_n>=3" in sel and not is_gbb(sel):
         return False
      if not "pt_jet_4>30" in sel and not is_gbb(sel):
         return False
      if "(signal_leptons_n)==0" in sel:
         if not "mT>=-1" in sel:
            return False
      else:
         if "mT>=-1" in sel:
            return False

   if doTest9:
      if not "met/meff_incl>=-1" in sel:
         return False
      if not "mTb_min>120" in sel:
         return False
      #if not "met>350" in sel:
      #   return False
      if not is_gbb(sel) and not is_low_meff(string):
         if "MJSum_rc_r08pt10>-1" in sel: 
            return False
      #else:
      #   if not "MJSum_rc_r08pt10>-1" in sel:
      #      return False
      if not "bjets_n>=3" in sel and not is_gbb(sel):
         return False
      #if not "pt_jet_4>30" in sel and not is_gbb(sel):
      #   return False
      if "(signal_leptons_n)==0" in sel:
         if not "mT>=-1" in sel:
            return False
      else:
         if not "mT>=150" in sel:
            return False


   if doTest8:
      if not "met/meff_incl>=-1" in sel:
         return False
      if not "mTb_min>120" in sel:
         return False
      #if not "met>350" in sel:
      #   return False
      if not is_gbb(sel) and not is_low_meff(string):
         if "MJSum_rc_r08pt10>-1" in sel: 
            return False
      #else:
      #   if not "MJSum_rc_r08pt10>-1" in sel:
      #      return False
      if not "bjets_n>=3" in sel:
         return False
      #if not "pt_jet_4>30" in sel and not is_gbb(sel):
      #   return False
      if "(signal_leptons_n)==0" in sel:
         if not "mT>=-1" in sel:
            return False
      else:
         if not "mT>=150" in sel:
            return False

   if doTest7:
      if not "met/meff_incl>=-1" in sel:
         return False
      if not "mTb_min>120" in sel:
         return False
      #if not "met>350" in sel:
      #   return False
      if not is_gbb(sel) and not is_low_meff(string):
         if "MJSum_rc_r08pt10>-1" in sel: 
            return False
      #else:
      #   if not "MJSum_rc_r08pt10>-1" in sel:
      #      return False
      if not "bjets_n>=3" in sel:
         return False
      #if not "pt_jet_4>30" in sel and not is_gbb(sel):
      #   return False
      if "(signal_leptons_n)==0" in sel:
         if not "mT>=-1" in sel:
            return False
      else:
         if "mT>=-1" in sel:
            return False



   if doTest6:
      if not "met/meff_incl>=-1" in sel:
         return False
      if not "mTb_min>100" in sel:
         return False
      #if not "met>350" in sel:
      #   return False
      if not is_gbb(sel) and not is_low_meff(string):
         if "MJSum_rc_r08pt10>-1" in sel: 
            return False
      #else:
      #   if not "MJSum_rc_r08pt10>-1" in sel:
      #      return False
      if not "bjets_n>=3" in sel and not is_gbb(sel):
         return False
      #if not "pt_jet_4>30" in sel and not is_gbb(sel):
      #   return False
      if "(signal_leptons_n)==0" in sel:
         if not "mT>=-1" in sel:
            return False
      else:
         if "mT>=-1" in sel:
            return False


   if doTest5:
      if not "met/meff_incl>=-1" in sel:
         return False
      if not "mTb_min>120" in sel:
         return False
      #if not "met>350" in sel:
      #   return False
      if not is_gbb(sel) and not is_low_meff(string):
         if "MJSum_rc_r08pt10>-1" in sel: 
            return False
      #else:
      #   if not "MJSum_rc_r08pt10>-1" in sel:
      #      return False
      if not "bjets_n>=3" in sel and not is_gbb(sel):
         return False
      #if not "pt_jet_4>30" in sel and not is_gbb(sel):
      #   return False
      if "(signal_leptons_n)==0" in sel:
         if not "mT>=-1" in sel:
            return False
      else:
         if "mT>=-1" in sel:
            return False


   if doTest4:
      if not "met/meff_incl>=-1" in sel:
         return False
      if not "mTb_min>120" in sel:
         return False
      if not "met>350" in sel:
         return False
      if not is_gbb(sel) and not is_low_meff(string):
         if "MJSum_rc_r08pt10>-1" in sel: 
            return False
      #else:
      #   if not "MJSum_rc_r08pt10>-1" in sel:
      #      return False
      if not "bjets_n>=3" in sel and not is_gbb(sel):
         return False
      #if not "pt_jet_4>30" in sel and not is_gbb(sel):
      #   return False
      if "(signal_leptons_n)==0" in sel:
         if not "mT>=-1" in sel:
            return False
      else:
         if "mT>=-1" in sel:
            return False

   if doTest3:
      if not "met/meff_incl>=-1" in sel:
         return False
      if not "mTb_min>120" in sel:
         return False
      if not "met>350" in sel:
         return False
      if not is_gbb(sel) and not is_low_meff(string):
         if "MJSum_rc_r08pt10>-1" in sel: 
            return False
      #else:
      #   if not "MJSum_rc_r08pt10>-1" in sel:
      #      return False
      if not "bjets_n>=3" in sel and not is_gbb(sel):
         return False
      if not "pt_jet_4>30" in sel and not is_gbb(sel):
         return False
      if "(signal_leptons_n)==0" in sel:
         if not "mT>=-1" in sel:
            return False
      #else:
      #   if not "mT>=150" in sel:
      #      return False


   if doTest2:
      if not "met/meff_incl>=-1" in sel:
         return False
      if not "mTb_min>140" in sel:
         return False
      if not "met>300" in sel:
         return False
      if not is_gbb(sel) and not is_low_meff(string):
         if not "MJSum_rc_r08pt10>150" in sel: 
            return False
      else:
         if not "MJSum_rc_r08pt10>-1" in sel:
            return False
      if not "bjets_n>=3" in sel:
         return False
      if not "pt_jet_4>30" in sel and not is_gbb(sel):
         return False
      if "(signal_leptons_n)==0" in sel:
         if not "mT>=-1" in sel:
            return False
      else:
         if not "mT>=150" in sel:
            return False


   if doTest1:
      if not "met/meff_incl>=-1" in sel:
         return False
      if not "mTb_min>120" in sel:
         return False
      if not "met>350" in sel:
         return False
      if not is_gbb(sel) and not is_low_meff(string):
         if not "MJSum_rc_r08pt10>150" in sel: 
            return False
      else:
         if not "MJSum_rc_r08pt10>-1" in sel:
            return False
      if not "bjets_n>=3" in sel:
         return False
      if not "pt_jet_4>30" in sel:
         return False
      if "(signal_leptons_n)==0" in sel:
         if not "mT>=-1" in sel:
            return False
      else:
         if not "mT>=150" in sel:
            return False


   # ttbar > 60%
   #if elem[3]/elem[2] < 0.6:
   #   return False

   # mtbmin fix at 100
   #if not "mTb_min>100" in sel:
   #   return False

   #if not "met>300" in sel:
   #   return False

   # no mjsum
   #if not "MJSum_rc_r08pt10>-1" in sel: 
   #   return False

   #if not "bjets_n>=3" in sel:
   #   return False

   #if not "pt_jet_4>30" in sel and not is_gbb(sel):
   #   return False

   if "(signal_leptons_n)==0" in sel and not "mT>=-1" in sel:
      return False


   # imposing mtmmin (remove for 2L) # chiara
   #if "mTb_min>-1" in sel:
   #   return False

   # imposing mtmmin (remove for 2L) # chiara
   #if "mT>=-1" in sel and "2l" in string:
   #   return False
   
   # imposting MJSum # chiara: remove for test
   #meffsplit=sel.split("meff")
   #if len(meffsplit) < 4 and not is_gbb(sel):
   #   if "MJSum_rc_r08pt10>-1" in sel:
      #if not "MJSum_rc_r08pt10>150" in sel:
   #      return False
   
   return True

def readpickle(inputdir, string, out_name, signal):

   sel_sig_map=dict()
   print "Intput dir ", inputdir
   os.chdir(inputdir)
   i=0
   for mypickle in glob.glob("*"+string+"*.pickle"):
      print mypickle
      with open(mypickle, 'rb') as handle:   
         x = pickle.load(handle)
      for key in x.keys():
         #if x[key][0] > 0 and x[key][0] < 1.79769313486e+308:
         key_new=key
         #if "-1" in key:
         #   key_new=key_new.replace("-1", "0")
         if passes_criteria(x[key], signal, key, string):
            sel_sig_map[key_new]=x[key]
      i+=1
      #print i,mypickle
      #print "len tot ",len(sel_sig_map),"  len new ",len(x),"\n"
      #print(mypickle)
   os.chdir('/nfs/pic.es/user/c/crizzi/scratch2/susy_multib/compressed_regions/optimization_code')
   #pickle.dump(sel_sig_map, open( out_name, "wb" ) )      
   return sel_sig_map

def readbigpickle(sel_sig_map, signal, string):
   #print "\n\nREADING BIG BIG PICKLE!!!\n"
   sig_map = dict()
   for key in sel_sig_map:
   #   if passes_criteria(sel_sig_map[key], signal, key):
      #print key
      sig_map[key]=sel_sig_map[key][0][signal]
      
   pickle.dump(sel_sig_map, open( out_name+"_"+string+"_all_sig.pickle", "wb" ) )

   isel =0
   for key in sorted(sig_map,key=sig_map.__getitem__, reverse=True):
      #if sig_map[key] > 0 and sig_map[key] < 1.79769313486e+308:
      if sig_map[key] < 1.79769313486e+308:
         if isel > 0:
            break
         #print "\n\nBEST SELS:"
         print key
         print "significance for",signal,":",sig_map[key]
         print "signal events:", sel_sig_map[key][1][signal]
         print "total background:",sel_sig_map[key][2]
         #print "ttbar:",sel_sig_map[key][3],"pm",sel_sig_map[key][4],"  (rel err:",sel_sig_map[key][4]/sel_sig_map[key][3],")"
         #print sel_sig_map[key],"\n"
         isel += 1
   #return (key,key+" && z-ttbar=="+"{:.2f}".format(sel_sig_map[key][3])+" && z-backg=="+"{:.2f}".format(sel_sig_map[key][2])+" && zz-signal=="+"{:.2f}".format(sel_sig_map[key][1][signal])+" && zz-signif=="+"{:.2f}".format(sig_map[key]) +" && z-ttbar-unc=="+"{:.2f}".format(sel_sig_map[key][4]/sel_sig_map[key][3])+" && z-ttbar-frac=="+"{:.2f}".format(sel_sig_map[key][3]/sel_sig_map[key][2])   )
   return (key,key+" && z-ttbar=="+"{:.2f}".format(sel_sig_map[key][3])+" && z-backg=="+"{:.2f}".format(sel_sig_map[key][2])+" && z-signal=="+"{:.2f}".format(sel_sig_map[key][1][signal])+" && z-ttbar-unc=="+"{:.2f}".format(sel_sig_map[key][4]/sel_sig_map[key][3])+" && z-ttbar-frac=="+"{:.2f}".format(sel_sig_map[key][3]/sel_sig_map[key][2])   )
   
   #print "\n\nFINE!!!\n\n"


def printbigpickle(sel_sig_map, signal):
   print "\n\nprint BIG BIG PICKLE!!!\n"
   sig_map = dict()
   for key in sel_sig_map:
      print key
      #if passes_criteria(sel_sig_map[key], signal):
      sig_map[key]=sel_sig_map[key][0][signal]
   
   isel =0
   for key in sorted(sig_map,key=sig_map.__getitem__, reverse=True):
      #if sig_map[key] > 0 and sig_map[key] < 1.79769313486e+308:
      if sig_map[key] < 1.79769313486e+308:
         #print "\n\nBEST SELS:"
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

   #map_bins=dict()

   if do2L:
      map_bins = {
         "0l_4_6_j_meff_incl_700_1400":"Gbb_1900_1800",
         "0l_4_6_j_meff_incl_1400_2000":"Gbb_1900_600",
         "0l_4_6_j_meff_incl_2000":"Gbb_2100_1",

         "0l_7_8_j_meff_incl_700_1600":"Gtt_1900_1400",
         "0l_7_8_j_meff_incl_1600_2200":"Gtt_1900_600",
         "0l_7_8_j_meff_incl_2200":"Gtt_2100_1",

         "0l_9_j_meff_incl_700_1800":"Gtt_1900_1400",
         "0l_9_j_meff_incl_1800_2400":"Gtt_1900_600",
         "0l_9_j_meff_incl_2400":"Gtt_2100_1",

         "1l_excl_6_7_j_meff_incl_700_1600":"Gtt_1900_1400",
         "1l_excl_6_7_j_meff_incl_1600_2200":"Gtt_1900_600",
         "1l_excl_6_7_j_meff_incl_2200":"Gtt_2100_1",

         "1l_excl_8_j_meff_incl_700_1800":"Gtt_1900_1400",
         "1l_excl_8_j_meff_incl_1800_2400":"Gtt_1900_600",
         "1l_excl_8_j_meff_incl_2400":"Gtt_2100_1",

         "2l_5_7_j_meff_incl_600_1500":"Gtt_1900_1400",
         "2l_5_7_j_meff_incl_1500":"Gtt_2100_1",

         "2l_8_j_meff_incl_700_1700":"Gtt_1900_1400",
         "2l_8_j_meff_incl_1700":"Gtt_2100_1"
      }

   else:
      if doMeff4jForGbb:
         map_bins = {
            "0l_4_6_j_meff_4j_800_1400":"Gbb_1900_1400",
            #"0l_4_6_j_meff_4j_800_1400":"Gbb_1900_1200",
            "0l_4_6_j_meff_4j_1400_2000":"Gbb_1900_600",
            "0l_4_6_j_meff_4j_2000":"Gbb_2100_1",
                        
            "0l_7_8_j_meff_incl_800_1600":"Gtt_1900_1400",
            "0l_7_8_j_meff_incl_1600_2200":"Gtt_1900_600",
            "0l_7_8_j_meff_incl_2200":"Gtt_2100_1",
            
            "0l_9_j_meff_incl_900_1800":"Gtt_1900_1400",
            "0l_9_j_meff_incl_1800_2400":"Gtt_1900_600",
            "0l_9_j_meff_incl_2400":"Gtt_2100_1",
            
            "1l_6_7_j_meff_incl_800_1600":"Gtt_1900_1400",
            "1l_6_7_j_meff_incl_1600_2200":"Gtt_1900_600",
            "1l_6_7_j_meff_incl_2200":"Gtt_2100_1",
            
            "1l_8_j_meff_incl_900_1800":"Gtt_1900_1400",
            "1l_8_j_meff_incl_1800_2400":"Gtt_1900_600",
            "1l_8_j_meff_incl_2400":"Gtt_2100_1",
            }
      else:
         map_bins = {            
            "0l_4_6_j_meff_incl_800_1400":"Gbb_1900_1400",
            #"0l_4_6_j_meff_incl_800_1400":"Gbb_1900_1200",
            "0l_4_6_j_meff_incl_1400_2000":"Gbb_1900_600",
            "0l_4_6_j_meff_incl_2000":"Gbb_2100_1",
            
            "0l_7_8_j_meff_incl_800_1600":"Gtt_1900_1400",
            "0l_7_8_j_meff_incl_1600_2200":"Gtt_1900_600",
            "0l_7_8_j_meff_incl_2200":"Gtt_2100_1",
            
            "0l_9_j_meff_incl_900_1800":"Gtt_1900_1400",
            "0l_9_j_meff_incl_1800_2400":"Gtt_1900_600",
            "0l_9_j_meff_incl_2400":"Gtt_2100_1",
            
            "1l_6_7_j_meff_incl_800_1600":"Gtt_1900_1400",
            "1l_6_7_j_meff_incl_1600_2200":"Gtt_1900_600",
            "1l_6_7_j_meff_incl_2200":"Gtt_2100_1",
            
            "1l_8_j_meff_incl_900_1800":"Gtt_1900_1400",
            "1l_8_j_meff_incl_1800_2400":"Gtt_1900_600",
            "1l_8_j_meff_incl_2400":"Gtt_2100_1",
            }


   #sel_dict=dict()
   final_selections=dict()
   final_selections_table=dict()
   print ""
   for string in map_bins:
      print string
      sel_dict_string = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_multib/compressed_regions/output_01_08_noRazor', string, string+".pickle",map_bins[string])
      #sel_dict_string = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_multib/compressed_regions/output_01_08', string, string+".pickle",map_bins[string])
      final_selections[string]=readbigpickle(sel_dict_string, map_bins[string], string)[0]
      final_selections_table[string]=readbigpickle(sel_dict_string, map_bins[string], string)[1]
      #if string == "0l_7_8_j_meff_incl_2000_2500":
         #printbigpickle(sel_dict[string], map_bins[string])
      
      if final_selections[string]:
         #final_selections[string]=final_selections[string].replace("weight_mc*weight_lumi*weight_btag*weight_elec*weight_muon*weight_jvt*","")
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
   
   pickle.dump(final_selections, open( out_name+".pickle", "wb" ) )

