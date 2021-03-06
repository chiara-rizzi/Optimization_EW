import argparse
import os, sys
import ROOT
from ROOT import gROOT
import math
#from pdgRounding import pdgRound
from ROOT import RooStats
import itertools
import json

import read_tree
from read_tree import *

lumi = 36074.56 # forseen for Moriond 2017
reluncer = 0.3

folder="/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.33-4-0/"
sig_name=folder+"Sig_GGM_tag.2.4.33-4-0_nominal_hh4b.root"
bkg_name=folder+"Bkg_tag.2.4.33-4-0_Vjets220_nominal_3b_0L_met.root"
backgrounds=["Wjets","Zjets","SingleTop","ttbar","TopEW","diboson"]
masses = ["200","300","400","500","600","800"]

bkg_file = ROOT.TFile.Open(bkg_name,"READ")
sig_file = ROOT.TFile.Open(sig_name,"READ")

def which_mass(name):
    for m in masses:
        if m in name:
            #if "hh" in name:
            return "hh-"+m
            #elif "ZZ" in name:
            #    return "ZZ-"+m
            #else:
            #    return "Zh-"+m
    if "sum" in name:
        return "quad sum"
    return "none"

if __name__ == "__main__":

    ROOT.gStyle.SetOptStat(0) 
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gROOT.SetBatch(ROOT.kTRUE)

    #--treeType 'hh' --sigType 'hh4b' --comb 1 --pdf 'significances_binned_ttbar50.pdf'

    parser = argparse.ArgumentParser()
    parser.add_argument('--comb', default=0, type=int, help='If the regions are orthogonal, draw quadratic sum')
    parser.add_argument('--reg', default='hh', type=str, help='If this string is not in the reigon name, skip the region')
    parser.add_argument('--treeType', default='hh', type=str, help='read from hh or Zh sample? chosse hh or Zh')
    parser.add_argument('--sigType', default='hh4b', type=str, help='Which signal to look at?')
    parser.add_argument('--json', default='discovery_regions.json', type=str, help='Name of the pickle file with the region definition')
    parser.add_argument('--pdf', default='significances_discovery_regions.pdf', type=str, help='Name of the output pdf file')
    args = parser.parse_args()

    json_file=args.json
    out_name=args.pdf
    do_sum = args.comb
    tree_type=args.treeType
    sig_type=args.sigType

    sel_table=dict()    

    with open(json_file, 'rb') as handle:   
        x = json.load(handle)

    

    h = ROOT.TH1F("h","h",len(masses),0,len(masses))
    h.GetXaxis().SetTitle("m(#tilde{#chi})   [GeV]")
    h.GetYaxis().SetTitle("Significance")
    #h.GetXaxis().SetTitleSize(0.5)                                                                                                                                                                                
    for i in range(len(masses)):
        h.GetXaxis().SetBinLabel(i+1, masses[i])
    h.SetMaximum(8)
    h.SetMinimum(0.1)

    hs=list()
    isel=0
    for key in sorted(x.keys()):
        if "weight" in key:
            continue
        if not args.reg in key:
            continue
            #if not "VR" in key:
            #    continue
        if "plot" in key:
            continue
        print "------------------------------"
        print key
        sel = x[key]
        #sel = "("+sel+")*is_hh_4b"
        hs.append(ROOT.TH1F("h_sig_"+key,"h",len(masses),0,len(masses)))
        print sel
        # look at signal
        nsignal = dict()
        # look at background
        totbkg = 0
        nttbar = 0
        error_ttbar = 0
        nttbar_raw = 0
        for b in backgrounds:
            b = b+"_NoSys"
            t = bkg_file.Get(b)
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
        print "total bkg:",totbkg
        ibin = 1
        for m in masses:
            t_signal = sig_file.Get("GGM_"+tree_type+"_"+m+"_"+sig_type+"_NoSys")
            #t_signal = sig_file.Get("hh_"+m+"_hh4b_NoSys")
            if (not t_signal):
                print "GGM_hh_"+m+"_NoSys"+" not found"
                nsignal[m]=0.
                continue
            sel_sig = sel
                #sel_sig = sel_sig.replace("*weight_meff_low_mTb","")
            signal_tuple = integral_and_error(t_signal, sel_sig)
            nsignal[m]=signal_tuple[0]*lumi
            if "Zh" in sig_type:
                print "Zh! x2"
                nsignal[m]=nsignal[m]*2.0 # for Zh
            elif "ZZ" in sig_type:
                print "ZZ! x4"
                nsignal[m]=nsignal[m]*4.0 # for Zh
            #if nsignal[m]/totbkg > 0.2:
            signif = RooStats.NumberCountingUtils.BinomialExpZ(float(nsignal[m]),float(totbkg),0.3)
            
            print m, "nsig:",nsignal[m], "  S/B:",round((nsignal[m]/totbkg)*100,1),"%","  sig:", signif
            hs[isel].SetBinContent(ibin, signif)
            ibin+=1
        isel+=1

    leg=ROOT.TLegend(0.13,0.6,0.31,0.89)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    ih =0

    for myh in hs:
        for ibin in range(0,myh.GetNbinsX()+1):
            if  myh.GetBinContent(ibin) < 0:
                myh.SetBinContent(ibin, 0)    
    if do_sum:
        h_sum=hs[0].Clone("quadrature_sum")
        for ibin in range(0,h_sum.GetNbinsX()+1):
            bin_cont =0
            for myh in hs:
                bin_cont_appo = myh.GetBinContent(ibin)
                bin_cont += (bin_cont_appo*bin_cont_appo)
            h_sum.SetBinContent(ibin, math.sqrt(bin_cont))
        h_sum.SetLineStyle(3)
        hs.append(h_sum)

    for myh in hs:
        #print "legend for",sorted(x.keys())[ih]
        leg.AddEntry(myh, which_mass(myh.GetName()), "l")
        ih+=1
    c = ROOT.TCanvas("significance")
    c.SetTicky()
    c.cd()
    h.Draw()
    leg.Draw()
    colors = [609, 856, 410, 801, 629, 879, 602, 921, 622, 632 ]
    #colors=[ 800, 797, 810, 630, 898, 808, 616, 611, 880, 875,873, 600, 603, 591, 856, 432, 434, 436, 416, 419, 410, 920, 922, 400, 400-6, 400-1, 844]
    ih=0
    for myh in hs:
        #print sorted(x.keys())[ih], colors[ih]
        myh.SetLineColor(colors[ih])
        myh.SetLineWidth(3)
        myh.Draw("histo same")
        ih+=1
    c.Print(out_name)
