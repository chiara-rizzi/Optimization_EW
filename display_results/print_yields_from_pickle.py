import make_table
import argparse
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

lumi = 36074.56 # forseen for Moriond 2017
reluncer = 0.3

pickle_file="test_chiara.pickle"

folder="/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tagEW.2.4.28-1-0/"
sig_name=folder+"Sig_GGM_17_03_22_tagEW.2.4.28-1_nominal_aliases_skim_3b_EW.root"
bkg_name=folder+"bkg_tagEW.2.4.28-1_v3_nominal_aliases_skim_3b_EW.root"
backgrounds=["Wjets","Zjets","SingleTop","TopEW","ttbar"]
masses = ["130","150","200","300","400","500","600","800"]

bkg_file = ROOT.TFile.Open(bkg_name,"READ")
sig_file = ROOT.TFile.Open(sig_name,"READ")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--reg', default='0', type=str, help='')
    parser.add_argument('--meffRw', default=False, type=bool, help='')
    parser.add_argument('--doTable', default=False, type=bool, help='')
    parser.add_argument('--sigCont', default=True, type=bool, help='')
    parser.add_argument('--printAllBkg', default=True, type=bool, help='')

    args = parser.parse_args()

    do_print_bkg_yields=True
    do_signal_contamination=args.sigCont
    do_add_weight_meff=args.meffRw
    do_table=args.doTable
    do_print_all_bkg=args.printAllBkg

    sel_table=dict()    

    with open(pickle_file, 'rb') as handle:   
        x = pickle.load(handle)
        
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
        """
        if do_add_weight_meff:
            sel = "("+sel+")*(weight_mc*weight_lumi*weight_btag*weight_elec*weight_muon*weight_jvt*weight_WZ_2_2*meff_rw_1L_QCD*weight_qcd_scale*seednom*meff_rw_0L_QCD)"
        else:
            sel = "("+sel+")*(weight_mc*weight_lumi*weight_btag*weight_elec*weight_muon*weight_jvt*weight_WZ_2_2*weight_qcd_scale*seednom)"
        if is_2_2_24:
            sel=sel.replace("*weight_qcd_scale*seednom","")
            sel=sel.replace("*meff_rw_1L_QCD","*weight_meff_low_mTb")
            """
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
            if do_print_bkg_yields and do_print_all_bkg:
                print b, bkg_tuple[0]*lumi
            if "ttbar" in b:
            #print "this is ttbar!"
                nttbar += (bkg_tuple[0]*lumi)
                error_ttbar += (bkg_tuple[1]*lumi)*(bkg_tuple[1]*lumi)
                nttbar_raw += bkg_tuple[2]
                error_ttbar = math.sqrt(error_ttbar)

        if do_print_bkg_yields:
            print "tot bkg:",totbkg
            print "ttbar:",nttbar
            print "ttbar unweighted:",nttbar_raw
            print "error_ttbar:",error_ttbar
            print "rel err tt:",error_ttbar/nttbar
            print "ttbar perc.:",nttbar/totbkg*100,"%"
            
        if do_signal_contamination:
            for m in masses:
                t_signal = sig_file.Get("GGM_hh_"+m+"_NoSys")
                if (not t_signal):
                    print "GGM_hh_"+m+"_NoSys"+" not found"
                    nsignal[m]=0.
                    continue
                sel_sig = sel
                #sel_sig = sel_sig.replace("*weight_meff_low_mTb","")
                signal_tuple = integral_and_error(t_signal, sel_sig)
                nsignal[m]=signal_tuple[0]*lumi
            #if nsignal[m]/totbkg > 0.2:
                #print m,nsignal[m], "S/B:",nsignal[m]/totbkg #,"sig:", RooStats.NumberCountingUtils.BinomialExpZ(float(nsignal[m]),float(totbkg),0.3)
                print m, "S/B:",round((nsignal[m]/totbkg)*100,1),"%"," sig:", RooStats.NumberCountingUtils.BinomialExpZ(float(nsignal[m]),float(totbkg),0.3)
                #print ""
        if do_table:
            print ""
            sel += " && z-ttbar=="+"{:.2f}".format(nttbar)+" && z-backg=="+"{:.2f}".format(totbkg)+" && z-ttbar-perc=="+"{:.2f}".format(nttbar/totbkg*100) 
            sel_table[key]=sel

    if do_table:
        out_name="output_"+args.reg
        f = open(out_name+".tex","w")
        table=make_table.make_table(sel_table,args.reg)    
        intro="\\documentclass[10pt,a4paper,landscape]{article} \n\\usepackage[utf8]{inputenc} \n\\usepackage[english]{babel} \n\\usepackage{amsmath} \n\\usepackage{amsfonts} \n\\usepackage{amssymb} \n\\usepackage{graphicx} \n\\begin{document} \n \\thispagestyle{empty} \n"
        closure="\\end{document} \n"
        
        f.write(intro)
        f.write(table)
        f.write(closure)
        f.close()

