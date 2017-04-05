
def make_table(mydict,request=""):
    sel_list={}    
    delimiters = ["==",">=","<=",">","<"]
    opposite_delimitesr = ["!=","<",">","<=",">="]

    for key in mydict:
        #print key
        string=mydict[key]
        if len(string)==0:
            continue
        string=string.replace("(","")
        string=string.replace(")","")
        string=string.replace(" ","")
        #print string
        mylist=string.split("&&")
        sel=dict()        

        for elem in mylist:
            #print elem
            val_var=[]
            found = False
            if "||" in elem:
                found = True
                #print "OR sel"
                or_elem=elem.split("||")                
                #print or_elem
                sel_appo=dict() 
                val_var_appo=list()
                for sub_elem in or_elem:
                    found2=False
                    for d in delimiters:
                        if d in sub_elem and not found2:
                            found2=True
                            val_var=sub_elem.split(d)
                            sel_appo[val_var[0]]="$"+d+"$ "+str(val_var[1])
                            val_var_appo.append(val_var)
                #print sel_appo
                sel[val_var_appo[0][0]] = sel_appo[val_var_appo[0][0]]+" or "+val_var_appo[1][0].replace("_","-")+" "+sel_appo[val_var_appo[1][0]]
                sel[val_var_appo[1][0]] = sel_appo[val_var_appo[1][0]]+" or "+val_var_appo[0][0].replace("_","-")+" "+sel_appo[val_var_appo[0][0]]
                #print sel
            for d in delimiters:                    
                if d in elem and not found:
                    val_var=elem.split(d)
                    found = True
                    if len(val_var)>0: 
                        add=""
                        #if "met/meff" in val_var[0]:
                            #print val_var[0],val_var[1]
                        #else:
                        if not "met/meff" in val_var[0]:
                            if "meff" in val_var[0] and ">" in d:
                                val_var[0]="meff"
                                add="_low"
                            elif "meff" in val_var[0] and "<" in d:
                                val_var[0]="meff"
                                add="_high"
                            elif "meff" in val_var[0]:
                                val_var[0]="meff"
                            elif val_var[0] == "jets_n" and ">" in d:
                                add="_low"
                            elif val_var[0] == "jets_n" and "<" in d:
                                add="_high"
                        sel[val_var[0]+add]="$"+d+"$ "+str(val_var[1])
        #print sel_list
        sel_list[key]=sel    
        
    def sort1L(word):
        return "1l" in word
    
    def Jetsort(word):
        sel=sel_list[word]["jets_n_low"]
        delimiters = ["==",">=","<=",">","<"]
        for d in delimiters:
            sel=sel.replace("$"+d+"$","")
        return float(sel)

    def Meffsort(word):
        #if "meff" in sel_list[word] and not "meff_high" in sel_list[word]:
            #if "meff_low" in sel_list[word]:
            #    sel=sel_list[word]["meff_low"]
            #else:
            #    sel=sel_list[word]["meff"]
        if not "meff_low" in sel_list[word]:
            sel_list[word]["meff_low"] = "0"
        sel=sel_list[word]["meff_low"]
        delimiters = ["==",">=","<=",">","<"]
        for d in delimiters:
            sel=sel.replace("$"+d+"$","")
        return float(sel)
        #else:
        #    return 0

    #print "before sorting"
    #print sel_list.keys()
    myregions=sorted(sorted(sel_list.keys(), key=Meffsort),key=Jetsort)
    #print "after sorting"
    #print myregions

    # look only at the regions that I am interested
    toremove=[]
    for reg in sorted(myregions):
        #print reg
        if len(request)>0:
            if not request in reg:
                toremove.append(reg)
    for reg in toremove:
        myregions.remove(reg)

# make list of variables for table
    myvars=[]
    for key in sel_list:
        for v in sel_list[key]:
            if "meff_4j" in v:
                v=v.replace("meff_4j","meff")
            if "meff_incl" in v and not "met/" in v:
                v=v.replace("meff_incl","meff")
            #if not v in myvars and not "_high" in v and not "_low" in v and not "tst_clean" in v:
            #if not v in myvars and not "tst_clean" in v and not "meff_high" in v and not "meff_low" in v and not "signif" in v and not "high" in v and not "low" in v:
            #if not v in myvars and not "tst_clean" in v and not "meff_high" in v and not "meff_low" in v and not "signif" in v and not "mDeltaR" in v and not "met/meff-incl" in v:
            if not v in myvars and not "tst_clean" in v and not "signif" in v and not "mDeltaR" in v and not "met/meff-incl" in v:
                myvars.append(v)
    #print myvars

    #print sel_list
    
    myregions=sorted(myregions)
    string = "\\resizebox{\\textwidth}{!}{"
    string+="\n"
    string+="\\begin{tabular}{|c|"
    for r in myregions:
        string+="c|"
    string+="}"
    string+="\n"
    string+="\\hline \n"
    string+=" "
    for r in myregions:
        string += " & "
        #string += r.replace("_","-").replace("0l-","").replace("1l-","").replace("meff-4j-","").replace("meff-incl-","")
        string += r.replace("_","-")
    string+=" \\\\"
    string+="\n \\hline \n"
    string+="\n \\hline \n"
    first_yield=False
    for  v in sorted(myvars):
        if "z-" in v and not first_yield:
            first_yield=True
            string+="\n \\hline \n"
        string+=v.replace("_","-").replace("zz-","").replace("z-","").replace("signal-electrons-n+signal-muons-n","lepton-n").replace("MJSum-rc-r08pt10","MJSum")
        for r in myregions:
            string+=" & "
            if v in sel_list[r].keys() and "-1" not in sel_list[r][v]:
                string+= sel_list[r][v]
            else:
                string+="-"
        string+=" \\\\"
        string+="\n \\hline \n"
    string+="\\end{tabular} \n } \n"

    return string


if __name__ == "__main__":

    testdict={}    
    testdict["1l_9_j_meff_4j_1700_2300"]="(trigger[12] && ((pt_jet_4>20 && MJSum_rc_r08pt10>150 && mTb_min>100 && bjets_n>=3 && mT>=150) && (((signal_electrons_n + signal_muons_n)>=1 && (jets_n>=9) && (meff_4j>=1700 && meff_4j<2300) && tst_clean==1) && (met>250))))"    
    testdict["1l_7_j_meff_4j_1700_2500"]="(trigger[12] && ((pt_jet_4>20 && MJSum_rc_r08pt10>150 && mTb_min>100 && bjets_n>=3 && mT>=150) && (((signal_electrons_n + signal_muons_n)>=1 && (jets_n>=7) && (meff_incl>=1700 && meff_incl<2300) && tst_clean==1) && (met>250))))"    
    testdict["0l_7_j_meff_incl_1700_2500"]="( meff_incl > 50 && trigger[12] && ((pt_jet_4>20 && MJSum_rc_r08pt10>150 && mTb_min>100 && bjets_n>=3 && mT>=150) && (((signal_electrons_n + signal_muons_n)>=1 && (jets_n>=7) && (meff_incl>=1700 && meff_incl<2300) && tst_clean==1) && (met>250))))"    
    testdict["0l_9_j_meff_incl_2300"]="(trigger[12] && ((pt_jet_4>70 && MJSum_rc_r08pt10>200 && mTb_min>-1 && bjets_n>=3 && mT>=150) && (((signal_electrons_n + signal_muons_n)>=1 && (jets_n>=9) && (meff_incl>=2300) && tst_clean==1) && (met>350))))"
    testdict["1l_9_j_meff_incl_900_1700"]="( meff_4j > 100 && trigger[12] && ((pt_jet_4>20 && MJSum_rc_r08pt10>-1 && mTb_min>80 && bjets_n>=3 && mT>=150) && (((signal_electrons_n + signal_muons_n)>=1 && (jets_n>=9) && (meff_incl>=900 && meff_incl<1700) && tst_clean==1) && (met>250))))"

    print make_table(testdict)
