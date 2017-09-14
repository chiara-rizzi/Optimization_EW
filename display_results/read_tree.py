# module with functions useful for optimization

import os, sys
import ROOT
from ROOT import gROOT
import math
#from pdgRounding import pdgRound
from ROOT import RooStats
import itertools

import pickle

def add_weight(sel):
  return "(weight_mc*weight_lumi*weight_btag*weight_elec*weight_muon*weight_jvt*weight_WZ_2_2)*("+sel+")"
  #return "(weight_mc*weight_lumi*weight_btag*weight_elec*weight_muon*weight_jvt*weight_WZ_2_2)*("+sel+")"


def add_trigger(sel):
  return "pass_MET && ("+sel+")"

def merge_sel(sel1,sel2):
  return "("+sel1+") && ("+sel2+")"

def integral_and_error(tree, sel):
  sel=add_weight(sel)
  if not tree:
    print "no tree"
  htmp=ROOT.TH1D("htmp","htmp",1,0,2)
  htmp.Sumw2()
  tree.Draw("1>>htmp",sel,"goff")
  n_weighted = htmp.GetBinContent(1)
  n_raw = htmp.GetEntries()
  #print "Events  = " , n_weighted
  error = ROOT.Double(0)
  integral = htmp.IntegralAndError(0,2,error)
  htmp.Clear()
  return (n_weighted, error, n_raw)

