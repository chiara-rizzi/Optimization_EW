# Optimization 
# * use RooStats::NumberCountinUtils::BinomialExpZ for the significance

import os, sys
import ROOT
from ROOT import gROOT
import math
#from pdgRounding import pdgRound
from ROOT import RooStats
import itertools

import pickle

import read_tree
from read_tree import *


lumi = 36074.56 
reluncer = 0.3

name_infile = "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.EW.2.4.28-3-3/bkg_tagEW.2.4.28-3-3_nominal.root"
name_infile_signal = "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.EW.2.4.28-3-3/Sig_GGM_tagEW.2.4.28-3-3_nominal_all_types.root"

# definition of the nj-meff bins
#pickle_sel_no_wei="/nfs/pic.es/user/c/crizzi/scratch2/susy_multib/compressed_regions/optimization_code/selections/sel_dict_01_08.pickle"

args=sys.argv

print args
print len(args)
for arg in args:
  print arg

def make_sel_list(bin_sel=""):
  all_cuts = list()
  all_cuts.append(["dphi_min>-1","dphi_min>0.5","dphi_min>0.6","dphi_min>0.7","dphi_min>1.0","dphi_min>1.5"]) # 6
  #all_cuts.append(("jets_n","<=",[5, 6, 7, 100])) # 4
  #all_cuts.append(["pt_jet_4>20","pt_jet_4>30"]) # 2
  all_cuts.append(("met_sig",">",[-1, 2.5, 5, 10, 15])) # 5
  all_cuts.append(("mTb_min",">",[-1, 80, 100, 120, 140, 160])) # 6 new
  #all_cuts.append(("met",">",[150,180,200,300,400,500])) # 6 new
  #all_cuts.append(("max(DeltaR_h1_dR,DeltaR_h2_dR)","<",[1, 1.25, 1.5, 1.75, 2, 2.5, 3, 3.5, 1000])) #9
  
  sel_list = make_sel_list_from_cuts(all_cuts,bin_sel)
  print "Number of combinations", len(sel_list)
  return sel_list

def check_sel(outputdictionary,backgrounds,masses,bin_sel=""):
  for sel in make_sel_list(bin_sel):
    print "\n--------------------------" 
    print "Considering selection\n" ,sel

def check_number(outputdictionary,backgrounds,masses,bin_sel=""):
  make_sel_list(bin_sel)
  

def run_optimization(outputdictionary,backgrounds,masses,bin_sel=""):

  print "in run_optimization"
  print "backgrounds"
  print backgrounds
  print "masses"
  print masses
  print "bin and met selection"
  print bin_sel
  print ""

######################################
  
  infile = ROOT.TFile.Open(name_infile,"READ")
  infile_signal = ROOT.TFile.Open(name_infile_signal,"READ")
  
  i = 0
  sel_sig_map = dict()

  m_time=ROOT.TStopwatch()
  m_time.Start()
  
  for sel in make_sel_list(bin_sel):                  
    #print "\n--------------------------" 
    #print "Considering selection\n\n" ,sel
    
    # look ar singnal
    nsignal = dict()
    for m in masses:
      #print m
      t_signal = infile_signal.Get(m+"_NoSys")
      if (not t_signal):
        #print m+"_NoSys"+" not found"
        nsignal[m]=0.
        continue
      signal_tuple = integral_and_error(t_signal, sel)
      nsignal[m]=signal_tuple[0]*lumi
      # chiara: per Zh e ZZ moltiplico come se fosse BR(chi chi -> ZZ) = 100% o BR(chi chi -> Zh) = 100%
      if "ZZ4b" in m or "ZZqqbb" in m or "ZZllbb" in m:
        nsignal[m]= nsignal[m]*4.0
      if "Zh4b" in m or "Zhqqbb" in m or "Zhllbb" in m:
        nsignal[m]= nsignal[m]*2.0

      #print m,signal_tuple[0]*lumi
      #if nsignal[m] < 2 : 
      #  nsignal[m] = 0
        
    # look at background
    totbkg = 0
    error_bkg = 0
    nttbar = 0
    error_ttbar = 0
    nttbar_raw = 0
    for b in backgrounds:
      b = b+"_NoSys"
      t = infile.Get(b)
      if (not t):
        print b,"not found"
        continue
      bkg_tuple = integral_and_error(t, sel)
      if bkg_tuple[0] > 0:
        totbkg += (bkg_tuple[0]*lumi)
      error_bkg += ((bkg_tuple[1]*lumi)*(bkg_tuple[1]*lumi))
      #print b, bkg_tuple[0]*lumi
      if "ttbar" in b:
        #print "this is ttbar!"
        nttbar += (bkg_tuple[0]*lumi)
        error_ttbar += (bkg_tuple[1]*lumi)*(bkg_tuple[1]*lumi)
        nttbar_raw += bkg_tuple[2]
    error_ttbar = math.sqrt(error_ttbar)
    error_bkg = math.sqrt(error_bkg)
    
    significance=dict()
    for m in masses:
      significance[m] = RooStats.NumberCountingUtils.BinomialExpZ(float(nsignal[m]),float(totbkg),reluncer)
      #print m,significance[m]
    
    #print "nttbar", nttbar
    #print "Significance ",significance
    sel_sig_map [sel] = (significance, nsignal, totbkg, nttbar, error_ttbar, nttbar_raw, error_bkg)
          
    #print "At selection #", i
          
    i = i+1                           
    #if i > 0:
    #  break
  #end of loop
	
  #print "Selezioni: ", i
  #print ""
  #print sel_sig_map
  #print ""

  print "Yeah! Done"

  with open(outputdictionary, 'wb') as handle:
    pickle.dump(sel_sig_map, handle)

  m_time.Stop()
  print "printing time  for ", i, " iterations \n"
  m_time.Print()


if __name__ == "__main__":

#  masses = ["GGM_hh_130","GGM_hh_150","GGM_hh_200","GGM_hh_300","GGM_hh_400","GGM_hh_500","GGM_hh_600","GGM_hh_800",
#          "GGM_Zh_130","GGM_Zh_150","GGM_Zh_200","GGM_Zh_300","GGM_Zh_400","GGM_Zh_500","GGM_Zh_600","GGM_Zh_800"]
  masses = ["GGM_hh_200_hh4b","GGM_hh_300_hh4b","GGM_hh_500_hh4b","GGM_hh_800_hh4b",
            "GGM_Zh_200_ZZ4b","GGM_Zh_300_ZZ4b","GGM_Zh_500_ZZ4b","GGM_Zh_800_ZZ4b",
            "GGM_Zh_200_Zh4b","GGM_Zh_300_Zh4b","GGM_Zh_500_Zh4b","GGM_Zh_800_Zh4b",
            "GGM_Zh_200","GGM_Zh_300","GGM_Zh_500","GGM_Zh_800",
            "GGM_Zh_200_ZZqqbb","GGM_Zh_300_ZZqqbb","GGM_Zh_500_ZZqqbb","GGM_Zh_800_ZZqqbb",
            "GGM_Zh_200_Zhqqbb","GGM_Zh_300_Zhqqbb","GGM_Zh_500_Zhqqbb","GGM_Zh_800_Zhqqbb",
            "GGM_Zh_200_ZZllbb","GGM_Zh_300_ZZllbb","GGM_Zh_500_ZZllbb","GGM_Zh_800_ZZllbb",
            "GGM_Zh_200_Zhllbb","GGM_Zh_300_Zhllbb","GGM_Zh_500_Zhllbb","GGM_Zh_800_Zhllbb"]

                  
  backgrounds=["Wjets","Zjets","SingleTop","ttbar","diboson","TopEW"]

    #bin_sel = bins_def[list_bins[index_bin]]
    #bin_sel = merge_sel(bin_sel,met_sel)
  outputdictionary="/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_05_01/dict_17_05_01.pickle"
  
  sel_extra=""
  i = -1
  for arg in args:
    i+=1
    if i == 0:
      continue
    if i == 1:
      sel_extra = arg
    if i > 1:
      sel_extra = merge_sel(sel_extra,arg)

  add_to_name=sel_extra.replace("==","_ug_").replace(" ","").replace("&&","").replace("=","").replace(">","_").replace("<","").replace(")(","_").replace(")","").replace("(","").replace("-","m")
  print add_to_name
  outputdictionary=outputdictionary.replace(".pickle","_"+add_to_name+".pickle")
  print outputdictionary
  #check_number(outputdictionary, backgrounds, masses, sel_extra)
  run_optimization(outputdictionary, backgrounds, masses, sel_extra)
