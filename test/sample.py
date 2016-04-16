# coding=utf-8

import sys
sys.path.append("../src")
from tnpy import RegexCore
import json;
#import tngraph as graph

core = RegexCore('../rules/cnext')
#graph.buildGraph(core,'time_fix');
#exit()
#RegexCore.LogFile = open("info.html", 'w')
#RegexCore.LogFile.truncate()

print(core.Extract('十三分之二十四',entities=[core.Entities['fraction']]))
read = open('chs.txt', 'r', encoding='utf-8')
lines = [x for x in read.readlines()]


for line in lines:
        r = core.Extract(line)
        js = json.dumps(r, indent=2, ensure_ascii=False);
        print(js);






#RegexCore.LogFile.flush()
#RegexCore.LogFile.close()