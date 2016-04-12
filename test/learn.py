# coding=utf-8

from src.tnpy import RegexCore
core = RegexCore('../rules/learn')
import src.tngraph as graph
graph.buildGraph(core,'int_0_99');
exit()
RegexCore.LogFile = open("learn.log", 'w')
RegexCore.LogFile.truncate()
#matchs=core.Match('领导你好！老婆你好');
#for m in matchs:
#    print('match',m.mstr, 'pos:',m.pos)


print(core.Rewrite('领导你好！老婆您好'));

print({r:core.Rewrite(r) for r in ['十','三十七','一十三','68']});

RegexCore.LogFile.flush()
RegexCore.LogFile.close()
