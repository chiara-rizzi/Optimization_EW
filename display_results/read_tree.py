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
  # IFAE top framework
  #return "weight_mc*weight_lumi*weight_lep*weight_jvt*("+sel+")"
  # official inputs
  return "weight_mc*weight_lumi*("+sel+")"


def add_trigger(sel):
  return "pass_MET && ("+sel+")"

def merge_sel(sel1,sel2):
  return "("+sel1+") && ("+sel2+")"

def integral_and_error(tree, sel):
  #print "in integral_and_error"
  #print sel
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

def make_sel_list_from_cuts(all_cuts, sel_to_add=""):  
  sel_list=[]
  sel =""
  all_cuts_dict = dict()
  for cut in all_cuts:
    all_cuts_dict[cut[0]]= list()    
  for cut in all_cuts:
    for step in cut[2]:
      step_sel = cut[0]+cut[1]+str(step)
      all_cuts_dict[cut[0]].append(step_sel)
  biglist = list()
  for key in all_cuts_dict:
    biglist.append(all_cuts_dict[key])
  mylist =  list(itertools.product(*biglist ))
  for sel_set in mylist:
    sel = ""
    for single_sel in sel_set:
      sel += single_sel
      sel += " && "
    sel = sel[:-4]
    if len(sel_to_add)>0:
      sel=merge_sel(sel,sel_to_add)
    sel=add_trigger(sel)
    #sel=add_weight(sel)
    sel_list.append(sel)
  return sel_list
