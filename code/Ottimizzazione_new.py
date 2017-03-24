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

name_infile = "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tagEW.2.4.28-1-0/bkg_tagEW.2.4.28-1_v3_nominal_aliases_skim_3b_EW.root"
name_infile_signal = "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tagEW.2.4.28-1-0/Sig_GGM_17_03_22_tagEW.2.4.28-1_nominal_aliases_skim_3b_EW.root"

# definition of the nj-meff bins
#pickle_sel_no_wei="/nfs/pic.es/user/c/crizzi/scratch2/susy_multib/compressed_regions/optimization_code/selections/sel_dict_01_08.pickle"

args=sys.argv

print args
print len(args)
for arg in args:
  print arg

def make_sel_list(bin_sel=""):
  all_cuts = list()


  #all_cuts.append(("met",">",[150,180,200,300,400,500,600])) # 7 new
  #all_cuts.append(("mTb_min",">",[-1, 80, 100, 120, 140, 160])) # 6 new
  #all_cuts.append(["pt_jet_4>20","pt_jet_4>30"])
  #all_cuts.append(("met_sig",">",[-1, 10, 15, 20])) # 7 new
  #all_cuts.append(["bjets_n_85>=3","bjets_n_85>=4","bjets_n_85==3",  "bjets_n_77>=3","bjets_n_77>=4","bjets_n_77==3","bjets_n_70>=3","bjets_n_70>=4","bjets_n_70==3","bjets_n_60>=3","bjets_n_60>=4","bjets_n_60==3"])
  #all_cuts.append(("jets_n","<=",[5, 6, 7, 100])) # 7 new
  #all_cuts.append(["dphi_min>0.4","dphi_min>0.75","dphi_min>1","dphi_min>1.25","dphi_min>1.5","dphi_min>0.4 && dphi_min<1","dphi_min>0.4 && dphi_min<0.75","dphi_min>0.4 && dphi_min<1.25"])
  #all_cuts.append(["max(DeltaR_h1_min_diff,DeltaR_h2_min_diff)<1","max(DeltaR_h1_min_diff,DeltaR_h2_min_diff)<1.5","max(DeltaR_h1_min_diff,DeltaR_h2_min_diff)<2","max(DeltaR_h1_min_diff,DeltaR_h2_min_diff)<2.5","max(DeltaR_h1_min_diff,DeltaR_h2_min_diff)<1000", "max(DeltaR_h1_115,DeltaR_h2_115)<1","max(DeltaR_h1_115,DeltaR_h2_115)<1.5","max(DeltaR_h1_115,DeltaR_h2_115)<2","max(DeltaR_h1_115,DeltaR_h2_115)<2.5","max(DeltaR_h1_115,DeltaR_h2_115)<1000", "max(DeltaR_h1_dR,DeltaR_h2_dR)<1","max(DeltaR_h1_dR,DeltaR_h2_dR)<1.5","max(DeltaR_h1_dR,DeltaR_h2_dR)<2","max(DeltaR_h1_dR,DeltaR_h2_dR)<2.5","max(DeltaR_h1_dR,DeltaR_h2_dR)<1000"])
  #all_cuts.append(["fabs(mass_h1_dR-mass_h2_dR)<20","fabs(mass_h1_dR-mass_h2_dR)<40","fabs(mass_h1_dR-mass_h2_dR)<60","fabs(mass_h1_dR-mass_h2_dR)<1000",
  #                 "fabs(mass_h1_115-mass_h2_115)<20","fabs(mass_h1_115-mass_h2_115)<40","fabs(mass_h1_115-mass_h2_115)<60","fabs(mass_h1_115-mass_h2_115)<1000",
  #                 "fabs(mass_h1_min_diff-mass_h2_min_diff)<20","fabs(mass_h1_min_diff-mass_h2_min_diff)<40","fabs(mass_h1_min_diff-mass_h2_min_diff)<60","fabs(mass_h1_min_diff-mass_h2_min_diff)<1000"])
  #all_cuts.append(["((mass_h1_dR+mass_h2_dR)/2.)<140 && ((mass_h1_dR+mass_h2_dR)/2.)>100", "((mass_h1_dR+mass_h2_dR)/2.)<150 && ((mass_h1_dR+mass_h2_dR)/2.)>90", "((mass_h1_dR+mass_h2_dR)/2.)<130 && ((mass_h1_dR+mass_h2_dR)/2.)>100"])
  all_cuts.append(["bjets_n_85>=4","bjets_n_77>=4"])
  all_cuts.append(["met>200","met>300"])
  all_cuts.append(("jets_n","<=",[5, 6]))

  sel_list = make_sel_list_from_cuts(all_cuts,bin_sel)
  print "Number of combinations", len(sel_list)
  return sel_list

def check_sel(outputdictionary,backgrounds,masses,bin_sel=""):
    for sel in make_sel_list(bin_sel):
      print "\n--------------------------" 
      print "Considering selection\n" ,sel


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
    #print "\n\n--------------------------"
    print "\n--------------------------" 
    print "Considering selection\n\n" ,sel
    
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
      #print m,signal_tuple[0]*lumi
      #if nsignal[m] < 2 : 
      #  nsignal[m] = 0
        
    # look at background
    totbkg = 0
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
      totbkg += (bkg_tuple[0]*lumi)
      print b, bkg_tuple[0]*lumi
      if "ttbar" in b:
        #print "this is ttbar!"
        nttbar += (bkg_tuple[0]*lumi)
        error_ttbar += (bkg_tuple[1]*lumi)*(bkg_tuple[1]*lumi)
        nttbar_raw += bkg_tuple[2]
        error_ttbar = math.sqrt(error_ttbar)
        
    significance=dict()
    for m in masses:
      significance[m] = RooStats.NumberCountingUtils.BinomialExpZ(float(nsignal[m]),float(totbkg),reluncer)
      #print m,significance[m]
    
    print "nttbar", nttbar
    print "Significance ",significance
    sel_sig_map [sel] = (significance, nsignal, totbkg, nttbar, error_ttbar, nttbar_raw)
          
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

  masses = ["GGM_hh_130","GGM_hh_150","GGM_hh_200","GGM_hh_300","GGM_hh_400","GGM_hh_500","GGM_hh_600","GGM_hh_800"]
  backgrounds=["Wjets","Zjets","SingleTop","TopEW","ttbar"]

    #bin_sel = bins_def[list_bins[index_bin]]
    #bin_sel = merge_sel(bin_sel,met_sel)
  outputdictionary="/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle/dict_24_03_17_test.pickle"
  
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

  add_to_name=sel_extra.replace(" ","").replace("&&","").replace("=","").replace(">","_").replace("<","").replace(")(","_").replace(")","").replace("(","").replace("-","m")
  print add_to_name
  outputdictionary=outputdictionary.replace(".pickle","_"+add_to_name+".pickle")
  print outputdictionary
  check_sel(outputdictionary, backgrounds, masses, sel_extra)
  #run_optimization(outputdictionary, backgrounds, masses, sel_extra)
