#!/usr/bin/env python3
# coding: utf-8
import re

SVfile = "StandardizedVariants.txt"
OUT = "compatideo_sv_data.js"

SV=""
with open(SVfile, "r") as f:
    SV = f.read()

ls = SV.splitlines()
svversion = "{} ({})".format(ls[0].split("#")[1].strip(), ls[1].split("#")[1].strip())
print(svversion)
js_svversion = 'sv_version="{}";\n'.format(svversion.replace('"', ''))

cvdict = {}
repattern = re.compile(r"^([0-9A-Fa-f]+) ([0-9A-Fa-f]+); CJK COMPATIBILITY IDEOGRAPH-([0-9A-Fa-f]+);$")
for line in SV.split("# CJK compatibility ideographs")[1].splitlines():
    #if not line.startswith("#") and line.strip() != "":
    m = repattern.match(line)
    if m:
        dictval = r"\u{"+m.group(1)+r"}\u{"+m.group(2)+"}"
        dictkey = r"\u{"+m.group(3)+"}"
        cvdict[dictkey] = dictval

js_dict ="ci2sv_dict={"
for key in cvdict:
    js_dict+= '"{}":"{}",'.format(key, cvdict[key])
js_dict = js_dict[:-1]+"};\n" # Remove final comma

with open(OUT, "w") as w:
    w.write(js_svversion)
    w.write(js_dict)