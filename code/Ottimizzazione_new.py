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

name_infile = "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.33-4-0/Bkg_tag.2.4.33-4-0_Vjets220_nominal_3b_0L_met.root"
name_infile_signal = "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.33-4-0/Sig_GGM_tag.2.4.33-4-0_nominal_hh4b_3b_0L_met.root"

# definition of the nj-meff bins
#pickle_sel_no_wei="/nfs/pic.es/user/c/crizzi/scratch2/susy_multib/compressed_regions/optimization_code/selections/sel_dict_01_08.pickle"

args=sys.argv

print args
print len(args)
for arg in args:
  print arg

def make_sel_list(bin_sel=""):
  all_cuts = list()

  all_cuts.append(("mTb_min",">",[-1, 50, 80, 100, 130, 160])) # 6
  all_cuts.append(["pass_MET && mass_h1_dR>110 && mass_h1_dR<150 && mass_h2_dR>90 &&mass_h2_dR<140"])
  #all_cuts.append(("met",">",[200,250,300,400])) # 4
  all_cuts.append(("met_sig",">",[-1,3, 6, 9, 12])) # 5
  all_cuts.append(["bjets_n>=3", "bjets_n>=4"]) # 2
  #all_cuts.append(("meff_4bj",">",[500, 700, 900, 1100])) # 4
  all_cuts.append(("meff_4bj",">",[550, 600, 650, 750, 800, 850, 950, 1000, 1050, 1150, 1200])) # 4
  #all_cuts.append(["meff_4bj<10000000","meff_4bj<700","meff_4bj<900","meff_4bj<1100"]) #4
  all_cuts.append(("max(DeltaR_h1_dR,DeltaR_h2_dR)","<",[0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 2.0, 2.3, 2.5, 4, 10000])) # 15

  #all_cuts.append(["DeltaR_bb<0.75","DeltaR_bb<1","DeltaR_bb<1.25","DeltaR_bb<1.5","DeltaR_bb<2","DeltaR_bb<2.5","DeltaR_bb<3"]) #7
  #all_cuts.append(["met_sig>-1","met_sig>10","met_sig>15"]) #3
  #all_cuts.append(["jets_n>=2","jets_n<=3", "jets_n<=4", "jets_n<=5"]) # 4
  #all_cuts.append(["signal_leptons_n==2 && Z_OSLeps && jets_n>=2 && signal_leptons_n==2"])
  #all_cuts.append(["dphi_min>-1","dphi_min>0.4","dphi_min>0.7"]) # 3

  #all_cuts.append(["Z_pt>-1","Z_pt>50","Z_pt>75","Z_pt>100","Z_pt>125","Z_pt>150","Z_pt>175","Z_pt>200","Z_pt>250"]) #9
  #all_cuts.append(["meff_incl>-1","meff_incl>300","meff_incl>500","meff_incl>600","meff_incl>700","meff_incl>800","meff_incl>900","meff_incl>1000"]) #8
  
  #all_cuts.append(["bjets_n==0","bjets_n<=1"]) #2

  #all_cuts.append(["jets_n==2 && signal_leptons_n==2 && Z_OSLeps"]) #1

  #all_cuts.append(["met>-1 && pt_lep_1>30 && (signal_electron_trig_pass || signal_muon_trig_pass)","met>50 && pt_lep_1>30 && (signal_electron_trig_pass || signal_muon_trig_pass)","met>100 && pt_lep_1>30 && (signal_electron_trig_pass || signal_muon_trig_pass)","met>150 && pt_lep_1>30 && (signal_electron_trig_pass || signal_muon_trig_pass)","met>200 && pass_MET","met>250 && pass_MET","met>300 && pass_MET","met>350 && pass_MET","met>400 && pass_MET"]) #9

  #all_cuts.append(["dphi_min>0.4","dphi_min>0.5","dphi_min>0.7"]) # 3

  #all_cuts.append(["(baseline_electrons_n+baseline_muons_n)==0 && dphi_min>0.4 && pass_MET && jets_n>=4","signal_leptons_n==0 dphi_min>0.4 && pass_MET && jets_n>=4"])   # 2
  #all_cuts.append(["jets_n==2", "jets_n<=5","jets_n<=6", "jets_n<=7"]) # 4


  #all_cuts.append(["bjets_n>=3", "bjets_n>=4","bjets_n==3", "bjets_n_70>=3"]) # 4
  #all_cuts.append(["pass_MET && jets_n>=2"])
  #all_cuts.append(["pt_jet_4>25","pt_jet_4>40"]) # 2
  

  #all_cuts.append(["mass_h1_dR>100", "mass_h1_dR>110"])
  #all_cuts.append(["mass_h1_dR<140", "mass_h1_dR<150", "mass_h1_dR<160"])

  #all_cuts.append(["mass_h2_dR>90", "mass_h2_dR>100"])
  #all_cuts.append(["mass_h2_dR<120", "mass_h2_dR<130", "mass_h2_dR<140"])
  #all_cuts.append(["pt_jet_4>40","pt_jet_4>25"]) #2
  #all_cuts.append(("meff_4bj",">",[400, 600, 800, 1000, 1100, 1200])) # 6 new


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
        print m+"_NoSys"+" not found"
        nsignal[m]=0.
        continue
      signal_tuple = integral_and_error(t_signal, sel)
      nsignal[m]=signal_tuple[0]*lumi
      # chiara: per Zh e ZZ moltiplico come se fosse BR(chi chi -> ZZ) = 100% o BR(chi chi -> Zh) = 100%
      #if "ZZ4b" in m or "ZZqqbb" in m or "ZZllbb" in m:
      #  nsignal[m]= nsignal[m]*4.0
      #if "Zh4b" in m or "Zhqqbb" in m or "Zhllbb" in m:
      #  nsignal[m]= nsignal[m]*2.0

      #print m,signal_tuple[0]*lumi
      #if nsignal[m] < 2 : 
      #  nsignal[m] = 0
        
    # look at background
    totbkg = 0
    error_bkg = 0
    nindividual = dict()
    error_individual = dict()
    nindividual_raw = dict()
    for b in backgrounds:
      nindividual[b] = 0
      error_individual[b] = 0
      nindividual_raw[b] = 0
      b_tree = b+"_NoSys"
      t = infile.Get(b_tree)
      if (not t):
        print b,"not found"
        continue
      bkg_tuple = integral_and_error(t, sel)
      if bkg_tuple[0] > 0: # add only if >0
        n_events_wei=bkg_tuple[0]
        error_this_bkg = bkg_tuple[1]
        if "ttbar" in b:
          n_events_wei=n_events_wei*1.2
          error_this_bkg = error_this_bkg*1.2
        totbkg += (n_events_wei*lumi)
        nindividual[b] = (n_events_wei*lumi)
        error_individual[b] = error_this_bkg*lumi
        nindividual_raw[b] = bkg_tuple[2] 
        error_bkg += ((error_this_bkg*lumi)*(error_this_bkg*lumi))
    # end loop on bkg, the total error is the sqrt of the sum in quadrature  
    error_bkg = math.sqrt(error_bkg)
    
    significance=dict()
    #print "At selection #", i
    for m in masses:
      significance[m] = RooStats.NumberCountingUtils.BinomialExpZ(float(nsignal[m]),float(totbkg),reluncer)
      #print m,significance[m],nsignal[m]
    
    #print "nindividual", nindividual
    #print "Significance ",significance
    sel_sig_map [sel] = (significance, nsignal, totbkg, nindividual, error_individual, nindividual_raw, error_bkg)          
          
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
  masses = ["GGM_hh_200_hh4b","GGM_hh_300_hh4b","GGM_hh_400_hh4b","GGM_hh_500_hh4b","GGM_hh_600_hh4b","GGM_hh_700_hh4b","GGM_hh_800_hh4b","GGM_hh_900_hh4b","GGM_hh_1000_hh4b"]

                  
  backgrounds=["Wjets","Zjets","SingleTop","ttbar","diboson","TopEW"]

    #bin_sel = bins_def[list_bins[index_bin]]
    #bin_sel = merge_sel(bin_sel,met_sel)
  outputdictionary="/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/optimization_EW/output_pickle_17_09_03/dict_17_09_14.pickle"
  
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
