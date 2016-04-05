# coding=utf-8
from src.tnpy import RegexCore
import json;
core = RegexCore('../rules/cnext')
#RegexCore.LogFile = open("info.html", 'w')
#RegexCore.LogFile.truncate()


read = open('chs.txt', 'r', encoding='utf-8')
lines = [x for x in read.readlines()]


for line in lines:
        r = core.Extract(line)
        js = json.dumps(r, indent=2, ensure_ascii=False);
        print(js);






#RegexCore.LogFile.flush()
#RegexCore.LogFile.close()