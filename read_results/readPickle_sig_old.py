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
              "any":">",
              "no_mTb":"mTb_min>120>-1"
              }
#mysel = ["dR","ptj20","met_from_180","ex3b_btag85"]
#mysel = ["4b_btag70"]
mysel = ["any"]

name_out="/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/read_results/"+"dict"

#MaxUncBkg30
#ttbar50_MaxUnctt40
#name_out+="_tt_fullOpt_17_07_03_mbb_100_mZ80_100_lowttUnc_no_bins.json"
#name_out+="_tt_Zh2L_meff_bins_17_07_07_HighttUnc.json"
#name_out+="_4b_hh_dR_no_met180_45j.json"
name_out+="_hh4b_lep20_Zjets.json"

def passes_criteria(elem, signal, sel, string, mysel):
   # elem = (significance, nsignal, totbkg, nttbar, error_ttbar, nttbar_raw, error_bkg)
   # * at least 2 signal events (weighted)
   # at least 2 signal events
   #if elem[1][signal] < 2:
      #return False
   # there must be some background
   #if "bjets_n_85" not in sel:
   #   return False

   #if not "meff_4bj>900" in sel:
   #   return False

   #if not "bjets_n>=4" in sel:
   #   return False

   if not elem[2]>0.4:
      return False
   
   if elem[6]/elem[2] > 0.4:
      return False
   # ttbar > 60%
   if not (elem[3]["ttbar"]+elem[3]["Zjets"])>0:
      return False
   if (elem[3]["ttbar"])++elem[3]["Zjets"]/elem[2] < 0.50:
      return False

   #if not (elem[3]["ttbar"] + elem[3]["Zjets"])>0:
   #   return False
   #if (elem[3]["ttbar"] + elem[3]["Zjets"])/elem[2] < 0.7:
   #   return False
   # ttbar unc < 40%
   #if elem[4]["ttbar"]/elem[3]["ttbar"] > 0.40:
   #   #print "big uncertianty"
   #   return False

   # * ttbar rel stat unc < 0.3
   #if not elem[3] > 0:
      #print "no ttbar"
   #   return False

   #if "met>180" in sel:
   #   return False

   #if not "meff_incl>1200" in sel:
   #   return False

   #if not "jets_n<=4" in sel:
   #   return False

   #if not "mass_h1_dR>100 && mass_h1_dR<150 && mass_h2_dR>90 && mass_h2_dR<130" in sel:
   #   return False

   for s in mysel:
      if not s in selections:
         #print s,"not in selections"
         return False
      if selections[s].startswith("!"):
         if selections[s].replace("!","") in sel:
            #print "no sel"
            return False
      else:
         if not selections[s] in sel:
            #print "no sel"
            return False

   return True

def readpickle(inputdir, string, out_name, signal, list_signals, mysel):
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
            if not passes_criteria(x[key], mysig, key, string, mysel):
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
         print "total background:",sel_sig_map[key][2],"pm",sel_sig_map[key][6],"  (rel err:",sel_sig_map[key][6]/sel_sig_map[key][2],")"
         if sel_sig_map[key][3]["ttbar"]>0:
            print "ttbar:",sel_sig_map[key][3]["ttbar"],"pm",sel_sig_map[key][4]["ttbar"],"  (rel err:",sel_sig_map[key][4]["ttbar"]/sel_sig_map[key][3]["ttbar"],")"
            print "ttbar percentage:",(sel_sig_map[key][3]["ttbar"]/sel_sig_map[key][2])*100,"%"
         #print sel_sig_map[key],"\n"
         isel += 1
   #return (key,key+" && z-ttbar=="+"{:.2f}".format(sel_sig_map[key][3])+" && z-backg=="+"{:.2f}".format(sel_sig_map[key][2])+" && zz-signal=="+"{:.2f}".format(sel_sig_map[key][1][signal])+" && zz-signif=="+"{:.2f}".format(sig_map[key]) +" && z-ttbar-unc=="+"{:.2f}".format(sel_sig_map[key][4]/sel_sig_map[key][3])+" && z-ttbar-frac=="+"{:.2f}".format(sel_sig_map[key][3]/sel_sig_map[key][2])   )
         #return (key,key+" && z-ttbar=="+"{:.2f}".format(sel_sig_map[key][3])+" && z-backg=="+"{:.2f}".format(sel_sig_map[key][2])+" && z-signal=="+"{:.2f}".format(sel_sig_map[key][1][signal])+" && z-ttbar-unc=="+"{:.2f}".format(sel_sig_map[key][4]/sel_sig_map[key][3])+" && z-ttbar-frac=="+"{:.2f}".format(sel_sig_map[key][3]/sel_sig_map[key][2])   )
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


   #sel_dict=dict()
   final_selections=dict()
   final_selections_table=dict()

   #signals = ["300","400","500","800"]
   signals = ["200","300","500","600","800","900"]
   signal_list=[]
   #signal_list+=["GGM_Zh_"+s+"_ZZqqbb" for s in signals]
   #signal_list+=["GGM_Zh_"+s+"_Zhqqbb" for s in signals]
   #signal_list+=["GGM_Zh_"+s+"_ZZall" for s in signals]
   #signal_list+=["GGM_Zh_"+s+"_Zhllbb" for s in signals]
   #signal_list+=["GGM_Zh_"+s+"_Zh4b" for s in signals]
   #signal_list+=["GGM_ZZ_"+s+"_hh4b" for s in signals]
   signal_list+=["GGM_hh_"+s+"_hh4b" for s in signals]

   print "my signal list!"
   print signal_list

   ############################
   # 4b final state - VR-jets #
   ############################
   """
   str_sel_pickle_hh4b_200="*bjets_*_met_180met250_m_rho400_1_100m_rho400_1140m_rho400_2_100m_rho400_2140*"
   str_sel_pickle_hh4b_500="*bjets_*_met_250met400_m_rho400_1_100m_rho400_1140m_rho400_2_100m_rho400_2140*"
   str_sel_pickle_hh4b_800="*bjets_*_met_400_m_rho400_1_100m_rho400_1140m_rho400_2_100m_rho400_2140*"

   str_sel_pickle_Zh4b_200="*bjets_*_met_180met250_m_rho400_1_100m_rho400_1140m_rho400_2_70m_rho400_2100*"
   str_sel_pickle_Zh4b_500="*bjets_*_met_250met400_m_rho400_1_100m_rho400_1140m_rho400_2_70m_rho400_2100*"
   str_sel_pickle_Zh4b_800="*bjets_*_met_400_m_rho400_1_100m_rho400_1140m_rho400_2_70m_rho400_2100*"

   str_sel_pickle_ZZ4b_200="*bjets_*_met_180met250_m_rho400_1_70m_rho400_1100m_rho400_2_70m_rho400_2100*"
   str_sel_pickle_ZZ4b_500="*bjets_*_met_250met400_m_rho400_1_70m_rho400_1100m_rho400_2_70m_rho400_2100*"
   str_sel_pickle_ZZ4b_800="*bjets_*_met_400_m_rho400_1_70m_rho400_1100m_rho400_2_70m_rho400_2100*"

   sel_dict_string_hh4b_200 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_06_03', str_sel_pickle_hh4b_200, "outpu_not_used.pickle","",signal_list, mysel)
   sel_dict_string_hh4b_500 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_06_03', str_sel_pickle_hh4b_500, "outpu_not_used.pickle","",signal_list, mysel)
   sel_dict_string_hh4b_800 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_06_03', str_sel_pickle_hh4b_800, "outpu_not_used.pickle","",signal_list, mysel)

   sel_dict_string_Zh4b_200 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_06_03', str_sel_pickle_Zh4b_200, "outpu_not_used.pickle","",signal_list, mysel)
   sel_dict_string_Zh4b_500 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_06_03', str_sel_pickle_Zh4b_500, "outpu_not_used.pickle","",signal_list, mysel)
   sel_dict_string_Zh4b_800 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_06_03', str_sel_pickle_Zh4b_800, "outpu_not_used.pickle","",signal_list, mysel)

   sel_dict_string_ZZ4b_200 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_06_03', str_sel_pickle_ZZ4b_200, "outpu_not_used.pickle","",signal_list, mysel)
   sel_dict_string_ZZ4b_500 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_06_03', str_sel_pickle_ZZ4b_500, "outpu_not_used.pickle","",signal_list, mysel)
   sel_dict_string_ZZ4b_800 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_06_03', str_sel_pickle_ZZ4b_800, "outpu_not_used.pickle","",signal_list, mysel)

   final_selections["hh4b_200"]=readbigpickle(sel_dict_string_hh4b_200, "GGM_hh_200_hh4b", "")[0]
   final_selections["hh4b_500"]=readbigpickle(sel_dict_string_hh4b_500, "GGM_hh_500_hh4b", "")[0]
   final_selections["hh4b_800"]=readbigpickle(sel_dict_string_hh4b_800, "GGM_hh_800_hh4b", "")[0]

   final_selections["Zh4b_200"]=readbigpickle(sel_dict_string_Zh4b_200, "GGM_Zh_200_Zh4b", "")[0]
   final_selections["Zh4b_500"]=readbigpickle(sel_dict_string_Zh4b_500, "GGM_Zh_500_Zh4b", "")[0]
   final_selections["Zh4b_800"]=readbigpickle(sel_dict_string_Zh4b_800, "GGM_Zh_800_Zh4b", "")[0]

   final_selections["ZZ4b_200"]=readbigpickle(sel_dict_string_ZZ4b_200, "GGM_Zh_300_ZZ4b", "")[0]
   final_selections["ZZ4b_500"]=readbigpickle(sel_dict_string_ZZ4b_500, "GGM_Zh_500_ZZ4b", "")[0]
   final_selections["ZZ4b_800"]=readbigpickle(sel_dict_string_ZZ4b_800, "GGM_Zh_800_ZZ4b", "")[0]


   #sel_dict_string4b = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_06_03', "*pass_METjets_n_4*mass_h1_dR_100mass_h1_dR140mass_h2_dR_100mass_h2_dR140*", "outpu_not_used.pickle","",signal_list, mysel)
   #final_selections["hh4b_200"]=readbigpickle(sel_dict_string4b, "GGM_hh_200_hh4b", "")[0]
   #final_selections["hh4b_500"]=readbigpickle(sel_dict_string4b, "GGM_hh_500_hh4b", "")[0]
   #final_selections["hh4b_800"]=readbigpickle(sel_dict_string4b, "GGM_hh_800_hh4b", "")[0]

   #final_selections["Zh4b_200"]=readbigpickle(sel_dict_string4b, "GGM_Zh_200_Zh4b", "")[0]
   #final_selections["Zh4b_500"]=readbigpickle(sel_dict_string4b, "GGM_Zh_500_Zh4b", "")[0]
   #final_selections["Zh4b_800"]=readbigpickle(sel_dict_string4b, "GGM_Zh_800_Zh4b", "")[0]

   #final_selections["ZZ4b_200"]=readbigpickle(sel_dict_string4b, "GGM_Zh_300_ZZ4b", "")[0]
   #final_selections["ZZ4b_500"]=readbigpickle(sel_dict_string4b, "GGM_Zh_500_ZZ4b", "")[0]
   #final_selections["ZZ4b_800"]=readbigpickle(sel_dict_string4b, "GGM_Zh_800_ZZ4b", "")[0]
   """


   ##################
   # 4b final state #
   ##################

   str_sel_pickle_4b="*_electrons_n*"
   sel_dict_string4b=readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_09_03', str_sel_pickle_4b, "outpu_not_used.pickle","",signal_list, mysel) 

   final_selections["hh4b_200"]=readbigpickle(sel_dict_string4b, "GGM_hh_200_hh4b", "")[0]
   final_selections["hh4b_300"]=readbigpickle(sel_dict_string4b, "GGM_hh_300_hh4b", "")[0]
   final_selections["hh4b_500"]=readbigpickle(sel_dict_string4b, "GGM_hh_500_hh4b", "")[0]
   final_selections["hh4b_800"]=readbigpickle(sel_dict_string4b, "GGM_hh_800_hh4b", "")[0]
   final_selections["hh4b_900"]=readbigpickle(sel_dict_string4b, "GGM_hh_900_hh4b", "")[0]


   str_sel_pickle_hh4b_200="met_180met250_mass_h1_dR_100mass_h1_dR140mass_h2_dR_100mass_h2_dR140*"
   str_sel_pickle_hh4b_500="met_250met400_mass_h1_dR_100mass_h1_dR140mass_h2_dR_100mass_h2_dR140*"
   str_sel_pickle_hh4b_800="met_400_mass_h1_dR_100mass_h1_dR140mass_h2_dR_100mass_h2_dR140*"

   str_sel_pickle_Zh4b_200="*pass_METjets_n_4_met_180met250_mass_h1_dR_100mass_h1_dR140mass_h2_dR_70mass_h2_dR100*"
   str_sel_pickle_Zh4b_500="*pass_METjets_n_4_met_250met400_mass_h1_dR_100mass_h1_dR140mass_h2_dR_70mass_h2_dR100*"
   str_sel_pickle_Zh4b_800="*pass_METjets_n_4_met_400_mass_h1_dR_100mass_h1_dR140mass_h2_dR_70mass_h2_dR100*"

   str_sel_pickle_ZZ4b_200="*pass_METjets_n_4_met_180met250_mass_h1_dR_70mass_h1_dR100mass_h2_dR_70mass_h2_dR100*"
   str_sel_pickle_ZZ4b_500="*pass_METjets_n_4_met_250met400_mass_h1_dR_70mass_h1_dR100mass_h2_dR_70mass_h2_dR100*"
   str_sel_pickle_ZZ4b_800="*pass_METjets_n_4_met_400_mass_h1_dR_70mass_h1_dR100mass_h2_dR_70mass_h2_dR100*"

   #sel_dict_string_hh4b_200 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_15', str_sel_pickle_hh4b_200, "outpu_not_used.pickle","",signal_list, mysel)
   #sel_dict_string_hh4b_500 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_15', str_sel_pickle_hh4b_500, "outpu_not_used.pickle","",signal_list, mysel)
   #sel_dict_string_hh4b_800 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_15', str_sel_pickle_hh4b_800, "outpu_not_used.pickle","",signal_list, mysel)

   #sel_dict_string_Zh4b_200 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_15', str_sel_pickle_Zh4b_200, "outpu_not_used.pickle","",signal_list, mysel)
   #sel_dict_string_Zh4b_500 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_15', str_sel_pickle_Zh4b_500, "outpu_not_used.pickle","",signal_list, mysel)
   #sel_dict_string_Zh4b_800 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_15', str_sel_pickle_Zh4b_800, "outpu_not_used.pickle","",signal_list, mysel)

   #sel_dict_string_ZZ4b_200 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_15', str_sel_pickle_ZZ4b_200, "outpu_not_used.pickle","",signal_list, mysel)
   #sel_dict_string_ZZ4b_500 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_15', str_sel_pickle_ZZ4b_500, "outpu_not_used.pickle","",signal_list, mysel)
   #sel_dict_string_ZZ4b_800 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_15', str_sel_pickle_ZZ4b_800, "outpu_not_used.pickle","",signal_list, mysel)
   """
   final_selections["hh4b_200"]=readbigpickle(sel_dict_string_hh4b_200, "GGM_hh_200_hh4b", "")[0]
   final_selections["hh4b_500"]=readbigpickle(sel_dict_string_hh4b_500, "GGM_hh_500_hh4b", "")[0]
   final_selections["hh4b_800"]=readbigpickle(sel_dict_string_hh4b_800, "GGM_hh_800_hh4b", "")[0]

   final_selections["Zh4b_200"]=readbigpickle(sel_dict_string_Zh4b_200, "GGM_Zh_200_Zh4b", "")[0]
   final_selections["Zh4b_500"]=readbigpickle(sel_dict_string_Zh4b_500, "GGM_Zh_500_Zh4b", "")[0]
   final_selections["Zh4b_800"]=readbigpickle(sel_dict_string_Zh4b_800, "GGM_Zh_800_Zh4b", "")[0]

   final_selections["ZZ4b_200"]=readbigpickle(sel_dict_string_ZZ4b_200, "GGM_Zh_300_ZZ4b", "")[0]
   final_selections["ZZ4b_500"]=readbigpickle(sel_dict_string_ZZ4b_500, "GGM_Zh_500_ZZ4b", "")[0]
   final_selections["ZZ4b_800"]=readbigpickle(sel_dict_string_ZZ4b_800, "GGM_Zh_800_ZZ4b", "")[0]
   """
   
   #sel_dict_string_test = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_06_13', "*", "outpu_not_used.pickle","",signal_list, mysel)
   #mystring="*_mass_h1_dR_70_mass_h1_dR110_mass_h2_dR_60_mass_h2_dR90*"
   mystring="*_mass_h1_*dR*"
   #sel_dict_string_test = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_07_07', mystring, "outpu_not_used.pickle","",signal_list, mysel)

   #print "hh"
   #final_selections["SR_hh4b_300"]=readbigpickle(sel_dict_string_test, "GGM_hh_300_hh4b", "")[0]
   #final_selections["SR_hh4b_400"]=readbigpickle(sel_dict_string_test, "GGM_hh_400_hh4b", "")[0]
   #final_selections["SR_hh4b_500"]=readbigpickle(sel_dict_string_test, "GGM_hh_500_hh4b", "")[0]
   #final_selections["SR_hh4b_800"]=readbigpickle(sel_dict_string_test, "GGM_hh_800_hh4b", "")[0]
   #print "Zh"
   #final_selections["SR_Zh4b_300"]=readbigpickle(sel_dict_string_test, "GGM_Zh_300_Zh4b", "")[0]
   #final_selections["SR_Zh4b_400"]=readbigpickle(sel_dict_string_test, "GGM_Zh_400_Zh4b", "")[0]
   #final_selections["SR_Zh4b_500"]=readbigpickle(sel_dict_string_test, "GGM_Zh_500_Zh4b", "")[0]
   #final_selections["SR_Zh4b_800"]=readbigpickle(sel_dict_string_test, "GGM_Zh_800_Zh4b", "")[0]
   #print "ZZ"
   #final_selections["SR_ZZ4b_300"]=readbigpickle(sel_dict_string_test, "GGM_ZZ_300_hh4b", "")[0]
   #final_selections["SR_ZZ4b_400"]=readbigpickle(sel_dict_string_test, "GGM_ZZ_400_hh4b", "")[0]
   #final_selections["SR_ZZ4b_500"]=readbigpickle(sel_dict_string_test, "GGM_ZZ_500_hh4b", "")[0]
   #final_selections["SR_ZZ4b_600"]=readbigpickle(sel_dict_string_test, "GGM_ZZ_600_hh4b", "")[0]
   #final_selections["SR_ZZ4b_800"]=readbigpickle(sel_dict_string_test, "GGM_ZZ_800_hh4b", "")[0]


   """
   sel_dict_string4b = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_15', "*pass_METjets_n_4*mass_h1_dR_100mass_h1_dR140mass_h2_dR_100mass_h2_dR140*", "outpu_not_used.pickle","",signal_list, mysel)
   final_selections["hh4b_200"]=readbigpickle(sel_dict_string4b, "GGM_hh_200_hh4b", "")[0]
   #final_selections["hh4b_500"]=readbigpickle(sel_dict_string4b, "GGM_hh_500_hh4b", "")[0]
   #final_selections["hh4b_800"]=readbigpickle(sel_dict_string4b, "GGM_hh_800_hh4b", "")[0]

   #final_selections["Zh4b_200"]=readbigpickle(sel_dict_string4b, "GGM_Zh_200_Zh4b", "")[0]
   #final_selections["Zh4b_500"]=readbigpickle(sel_dict_string4b, "GGM_Zh_500_Zh4b", "")[0]
   #final_selections["Zh4b_800"]=readbigpickle(sel_dict_string4b, "GGM_Zh_800_Zh4b", "")[0]

   #final_selections["ZZ4b_200"]=readbigpickle(sel_dict_string4b, "GGM_Zh_300_ZZ4b", "")[0]
   #final_selections["ZZ4b_500"]=readbigpickle(sel_dict_string4b, "GGM_Zh_500_ZZ4b", "")[0]
   #final_selections["ZZ4b_800"]=readbigpickle(sel_dict_string4b, "GGM_Zh_800_ZZ4b", "")[0]
   """

   ####################
   # qqbb final state #
   ####################
   """
   str_sel_pickle_ZZqqbb_200="*_met_180met250_mass_bb_70mass_bb100mass_jj_70mass_jj100*"
   str_sel_pickle_ZZqqbb_500="*_met_250met400_mass_bb_70mass_bb100mass_jj_70mass_jj100*"
   str_sel_pickle_ZZqqbb_800="*_met_400_mass_bb_70mass_bb100mass_jj_70mass_jj100*"

   str_sel_pickle_Zhqqbb_200="*_met_180met250_mass_bb_100mass_bb140mass_jj_70mass_jj100*"
   str_sel_pickle_Zhqqbb_500="*_met_250met400_mass_bb_100mass_bb140mass_jj_70mass_jj100*"
   str_sel_pickle_Zhqqbb_800="*_met_400_mass_bb_100mass_bb140mass_jj_70mass_jj100*"

   #sel_dict_string_ZZqqbb_200 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_01', str_sel_pickle_ZZqqbb_200, "outpu_not_used.pickle","",signal_list, mysel)
   #sel_dict_string_ZZqqbb_500 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_01', str_sel_pickle_ZZqqbb_500, "outpu_not_used.pickle","",signal_list, mysel)
   sel_dict_string_ZZqqbb_800 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_01', str_sel_pickle_ZZqqbb_800, "outpu_not_used.pickle","",signal_list, mysel)

   #sel_dict_string_Zhqqbb_200 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_01', str_sel_pickle_Zhqqbb_200, "outpu_not_used.pickle","",signal_list, mysel)
   #sel_dict_string_Zhqqbb_500 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_01', str_sel_pickle_Zhqqbb_500, "outpu_not_used.pickle","",signal_list, mysel)
   #sel_dict_string_Zhqqbb_800 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_01', str_sel_pickle_Zhqqbb_800, "outpu_not_used.pickle","",signal_list, mysel)

   #final_selections["ZZqqbb_200"]=readbigpickle(sel_dict_string_ZZqqbb_200, "GGM_Zh_200_ZZqqbb", "")[0]
   #final_selections["ZZqqbb_500"]=readbigpickle(sel_dict_string_ZZqqbb_500, "GGM_Zh_500_ZZqqbb", "")[0]
   final_selections["ZZqqbb_800"]=readbigpickle(sel_dict_string_ZZqqbb_800, "GGM_Zh_800_ZZqqbb", "")[0]

   #final_selections["Zhqqbb_200"]=readbigpickle(sel_dict_string_Zhqqbb_200, "GGM_Zh_200_Zhqqbb", "")[0]
   #final_selections["Zhqqbb_500"]=readbigpickle(sel_dict_string_Zhqqbb_500, "GGM_Zh_500_Zhqqbb", "")[0]
   #final_selections["Zhqqbb_800"]=readbigpickle(sel_dict_string_Zhqqbb_800, "GGM_Zh_800_Zhqqbb", "")[0]
   """
   """
   str_sel_pickle_qqbb="*mass_bb*mass_jj*"
   sel_dict_string_qqbb=readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_01', str_sel_pickle_qqbb, "outpu_not_used.pickle","",signal_list, mysel) 
   final_selections["ZZqqbb_200"]=readbigpickle(sel_dict_string_qqbb, "GGM_Zh_200_ZZqqbb", "")[0]
   final_selections["ZZqqbb_500"]=readbigpickle(sel_dict_string_qqbb, "GGM_Zh_500_ZZqqbb", "")[0]
   final_selections["ZZqqbb_800"]=readbigpickle(sel_dict_string_qqbb, "GGM_Zh_800_ZZqqbb", "")[0]

   final_selections["Zhqqbb_200"]=readbigpickle(sel_dict_string_qqbb, "GGM_Zh_200_Zhqqbb", "")[0]
   final_selections["Zhqqbb_500"]=readbigpickle(sel_dict_string_qqbb, "GGM_Zh_500_Zhqqbb", "")[0]
   final_selections["Zhqqbb_800"]=readbigpickle(sel_dict_string_qqbb, "GGM_Zh_800_Zhqqbb", "")[0]
   """    




   ####################
   # llqq final state #
   ####################
   #str_sel_pickle_qqbb="*Z_mass*"
   #sel_dict_string_all=readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_07_12', str_sel_pickle_qqbb, "outpu_not_used.pickle","",signal_list, mysel) 
   #final_selections["ZZall_300"]=readbigpickle(sel_dict_string_all, "GGM_Zh_300_ZZall", "")[0]
   #final_selections["ZZall_500"]=readbigpickle(sel_dict_string_all, "GGM_Zh_500_ZZall", "")[0]
   #final_selections["ZZall_150"]=readbigpickle(sel_dict_string_all, "GGM_Zh_150_ZZall", "")[0]
   #final_selections["ZZall_600"]=readbigpickle(sel_dict_string_all, "GGM_Zh_600_ZZall", "")[0]
   #final_selections["ZZall_800"]=readbigpickle(sel_dict_string_all, "GGM_Zh_800_ZZall", "")[0]


   ####################
   # llbb final state #
   ####################
   """
   str_sel_pickle_ZZllbb_200="*_met_180met250_mass_bb_70mass_bb100Z_mass_70Z_mass100*"
   str_sel_pickle_ZZllbb_500="*_met_250met400_mass_bb_70mass_bb100Z_mass_70Z_mass100*"
   str_sel_pickle_ZZllbb_800="*_met_400_mass_bb_70mass_bb100Z_mass_70Z_mass100*"

   str_sel_pickle_Zhllbb_200="*_met_180met250_mass_bb_100mass_bb140Z_mass_70Z_mass100*"
   str_sel_pickle_Zhllbb_500="*_met_250met400_mass_bb_100mass_bb140Z_mass_70Z_mass100*"
   str_sel_pickle_Zhllbb_800="*_met_400_mass_bb_100mass_bb140Z_mass_70Z_mass100*"

   sel_dict_string_ZZllbb_200 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_01', str_sel_pickle_ZZllbb_200, "outpu_not_used.pickle","",signal_list, mysel)
   sel_dict_string_ZZllbb_500 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_01', str_sel_pickle_ZZllbb_500, "outpu_not_used.pickle","",signal_list, mysel)
   sel_dict_string_ZZllbb_800 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_01', str_sel_pickle_ZZllbb_800, "outpu_not_used.pickle","",signal_list, mysel)

   sel_dict_string_Zhllbb200 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_01', str_sel_pickle_Zhllbb_200, "outpu_not_used.pickle","",signal_list, mysel)
   sel_dict_string_Zhllbb500 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_01', str_sel_pickle_Zhllbb_500, "outpu_not_used.pickle","",signal_list, mysel)
   sel_dict_string_Zhllbb800 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_01', str_sel_pickle_Zhllbb_800, "outpu_not_used.pickle","",signal_list, mysel)

   final_selections["ZZllbb_200"]=readbigpickle(sel_dict_string_ZZllbb_200, "GGM_Zh_200_ZZllbb", "")[0]
   final_selections["ZZllbb_500"]=readbigpickle(sel_dict_string_ZZllbb_500, "GGM_Zh_500_ZZllbb", "")[0]
   final_selections["ZZllbb_800"]=readbigpickle(sel_dict_string_ZZllbb_800, "GGM_Zh_800_ZZllbb", "")[0]

   final_selections["Zhllbb_200"]=readbigpickle(sel_dict_string_Zhllbb200, "GGM_Zh_200_Zhllbb", "")[0]
   final_selections["Zhllbb_500"]=readbigpickle(sel_dict_string_Zhllbb500, "GGM_Zh_500_Zhllbb", "")[0]
   final_selections["Zhllbb_800"]=readbigpickle(sel_dict_string_Zhllbb800, "GGM_Zh_800_Zhllbb", "")[0]
   """

   str_sel_pickle_llbb="*mass_bb100*Z_mass_80_Z_mass100*"
   #str_sel_pickle_llbb="*mass_bb_*Z_mass*"
   #sel_dict_string_llbb = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_07_03', str_sel_pickle_llbb, "outpu_not_used_tt_full_opt_17_07_03.pickle","",signal_list, mysel)
   #sel_dict_string_llbb = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_06_27/mass_bb_100', str_sel_pickle_llbb, "outpu_not_used_tt_full_opt_17_07_03.pickle","",signal_list, mysel)

   """
   final_selections["Zhllbb_200"]=readbigpickle(sel_dict_string_llbb, "GGM_Zh_200_Zhllbb", "")[0]
   final_selections["Zhllbb_300"]=readbigpickle(sel_dict_string_llbb, "GGM_Zh_300_Zhllbb", "")[0]
   final_selections["Zhllbb_400"]=readbigpickle(sel_dict_string_llbb, "GGM_Zh_400_Zhllbb", "")[0]
   final_selections["Zhllbb_500"]=readbigpickle(sel_dict_string_llbb, "GGM_Zh_500_Zhllbb", "")[0]

   """
   #final_selections["ZZllbb_200"]=readbigpickle(sel_dict_string_llbb, "GGM_Zh_200_ZZllbb", "")[0]
   #final_selections["ZZllbb_300"]=readbigpickle(sel_dict_string_llbb, "GGM_Zh_300_ZZllbb", "")[0]
   #final_selections["ZZllbb_400"]=readbigpickle(sel_dict_string_llbb, "GGM_Zh_400_ZZllbb", "")[0]
   #final_selections["ZZllbb_500"]=readbigpickle(sel_dict_string_llbb, "GGM_Zh_500_ZZllbb", "")[0]
   #final_selections["ZZllbb_800"]=readbigpickle(sel_dict_string_llbb, "GGM_Zh_800_ZZllbb", "")[0]
   #final_selections["Zhllbb_800"]=readbigpickle(sel_dict_string_llbb, "GGM_Zh_800_Zhllbb", "")[0]

   ##############################
   # llbb final state - VR jets #
   ##############################
   """
   str_sel_pickle_ZZllbb_200="*bjets_n_ug_2*_met_180met250_m_rho400_1_70m_rho400_1100*"
   str_sel_pickle_ZZllbb_500="*bjets_n_ug_2*_met_250met400_m_rho400_1_70m_rho400_1100*"
   str_sel_pickle_ZZllbb_800="*bjets_n_ug_2*_met_400_m_rho400_1_70m_rho400_1100*"

   str_sel_pickle_Zhllbb_200="*bjets_n_ug_2*_met_180met250_m_rho400_1_100m_rho400_1140*"
   str_sel_pickle_Zhllbb_500="*bjets_n_ug_2*_met_250met400_m_rho400_1_100m_rho400_1140*"
   str_sel_pickle_Zhllbb_800="*bjets_n_ug_2*_met_400_m_rho400_1_100m_rho400_1140*"

   sel_dict_string_ZZllbb_200 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_06_03', str_sel_pickle_ZZllbb_200, "outpu_not_used.pickle","",signal_list, mysel)
   sel_dict_string_ZZllbb_500 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_06_03', str_sel_pickle_ZZllbb_500, "outpu_not_used.pickle","",signal_list, mysel)
   sel_dict_string_ZZllbb_800 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_06_03', str_sel_pickle_ZZllbb_800, "outpu_not_used.pickle","",signal_list, mysel)

   sel_dict_string_Zhllbb200 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_06_03', str_sel_pickle_Zhllbb_200, "outpu_not_used.pickle","",signal_list, mysel)
   sel_dict_string_Zhllbb500 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_06_03', str_sel_pickle_Zhllbb_500, "outpu_not_used.pickle","",signal_list, mysel)
   sel_dict_string_Zhllbb800 = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_06_03', str_sel_pickle_Zhllbb_800, "outpu_not_used.pickle","",signal_list, mysel)

   final_selections["ZZllbb_200"]=readbigpickle(sel_dict_string_ZZllbb_200, "GGM_Zh_200_ZZllbb", "")[0]
   final_selections["ZZllbb_500"]=readbigpickle(sel_dict_string_ZZllbb_500, "GGM_Zh_500_ZZllbb", "")[0]
   final_selections["ZZllbb_800"]=readbigpickle(sel_dict_string_ZZllbb_800, "GGM_Zh_800_ZZllbb", "")[0]

   final_selections["Zhllbb_200"]=readbigpickle(sel_dict_string_Zhllbb200, "GGM_Zh_200_Zhllbb", "")[0]
   final_selections["Zhllbb_500"]=readbigpickle(sel_dict_string_Zhllbb500, "GGM_Zh_500_Zhllbb", "")[0]
   final_selections["Zhllbb_800"]=readbigpickle(sel_dict_string_Zhllbb800, "GGM_Zh_800_Zhllbb", "")[0]

   str_sel_pickle_llbb="*mass_bb*Z_mass*"
   sel_dict_string_llbb = readpickle('/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_01', str_sel_pickle_llbb, "outpu_not_used.pickle","",signal_list, mysel)

   final_selections["ZZllbb_200"]=readbigpickle(sel_dict_string_llbb, "GGM_Zh_200_ZZllbb", "")[0]
   final_selections["ZZllbb_500"]=readbigpickle(sel_dict_string_llbb, "GGM_Zh_500_ZZllbb", "")[0]
   final_selections["ZZllbb_800"]=readbigpickle(sel_dict_string_llbb, "GGM_Zh_800_ZZllbb", "")[0]

   final_selections["Zhllbb_200"]=readbigpickle(sel_dict_string_llbb, "GGM_Zh_200_Zhllbb", "")[0]
   final_selections["Zhllbb_500"]=readbigpickle(sel_dict_string_llbb, "GGM_Zh_500_Zhllbb", "")[0]
   final_selections["Zhllbb_800"]=readbigpickle(sel_dict_string_llbb, "GGM_Zh_800_Zhllbb", "")[0]
   """



   print ""
   print ""
   print ""
   print ""
   print final_selections
   with open(name_out,"w") as outf:
      json.dump(final_selections, outf, indent=2)
   outf.close()


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


