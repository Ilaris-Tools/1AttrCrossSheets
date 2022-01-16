#!/usr/bin/env python3
from PyPDF2 import PdfFileReader
import random
import glob
import argparse
from dataclasses import dataclass

parser = argparse.ArgumentParser(description='Get pdf with highest value in ability/talent and said value.')
parser.add_argument('--search', '-s', dest='search', default="wahrnehmung/wachsamkeit",
                    help='Expects ability/talent; else it goes for wahrnehmung/wachsamkeit')
args = parser.parse_args()

@dataclass
class CharacterValues:
    """Class for keeping track of a character"""
    name: str
    cdict: dict

infiles = glob.glob("*.pdf")
random.shuffle(infiles)
chars = []
m = args.search

if(not infiles):
    print("No *.pdf in this folder...\nI go back to sleep. Zzz")

for file in infiles:
    with open(file, "rb") as content:
        pdf_reader = PdfFileReader(content)
        cdict = pdf_reader.getFormTextFields()
    chars.append(CharacterValues(name=file, cdict=cdict))
m = m.split("/")
m = m if len(m)>1 and not m[1] is "" else [m[0],"42"]
hName = "None"
hVal = -1
for cVal in chars:
    try:
        try:
            if(m[1] in cVal.cdict[m[0][:5]+"TA"]):
                rv = int(cVal.cdict[m[0][:5]+"PWT"])
            else:
                rv = int(cVal.cdict[m[0][:5]+"PW"])
            if(hVal < rv):
                hName = cVal.name
                hVal = rv
        except KeyError as e:
            na = None
            for num in range(1,29):
                if(cVal.cdict[f"Fertigkeit{num}NA"] == m[0]):
                    na = num
                    break
            if(na):
                if(m[1] in cVal.cdict[f"Fertigkeit{num}TA"]):
                    rv = int(cVal.cdict[f"Fertigkeit{num}PWT"])
                else:
                    rv = int(cVal.cdict[f"Fertigkeit{num}PW"])
                if(hVal < rv):
                    hName = cVal.name
                    hVal = rv
            else:
                raise KeyError
    except KeyError:
        print("Sure that said skill/talent exists?")
		
print(f"{hName}: {hVal}")
