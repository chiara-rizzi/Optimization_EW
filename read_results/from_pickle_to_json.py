import json
import pickle

pickle_name="pickle_selections_round1/dict_dR_ptj20_met_from_180_btag77.pickle"
json_name="dict_dR_ptj20_met_from_180_btag77.json"

with open(pickle_name,"r") as infile:
    mydict=pickle.load(infile)

with open(json_name,"wb") as outfile:
    json.dump(mydict, outfile, indent=2)
