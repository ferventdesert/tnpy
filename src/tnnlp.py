# encoding: UTF-8

from src.tnpy import StringEntity as SE, RegexEntity as RE, TableEntity as TE, SequenceEntity as SQE, RepeatEntity as RPE, \
    EntityBase

import jieba.posseg as pseg


wordlib={};


def initwordlib(path):
    read = open(path, 'r', 'utf-8')
    lines = [(x) for x in read.readlines()]
    for line in lines:
        ws=line.split(' ');
        name= ws[0];
        words= [w.strip() for w in ws[1:]];
        wordlib[name]=words;



class NEREntity(EntityBase):
    def __init__(self, pos=None, maxlen=-1):
        super(NEREntity, self).__init__()
        if isinstance(pos, str):
            self.Pos = [pos];
        elif isinstance(pos, list):
            self.Pos = pos;
        else:
            self.Pos = None;

        self.Len = maxlen;

    def RewriteItem(self, input):
        return input

    def MatchItem(self, input, start, end,muststart, mode=None):
        self.LogIn(input, start,end)
        pos = start;
        if end is None:
            end=len(input);
        seg_list = pseg.cut(input[start:end] if self.Len == -1 else input[start:start + self.Len]);
        for word, flag in seg_list:
            if self.Pos is None:
                sword = word;
                break;
            else:
                if flag in self.Pos:
                    sword = word;
                    break;
            pos += len(word);
        if pos < 0 or (muststart == True and pos != start):
            self.LogOut(None)
            return start + self.Len if self.Len < 0 else tnpy.int_max;
        self.LogOut(sword)
        m = tnpy.MatchResult(self, sword, pos);
        m.rstr = sword;
        return m;




class WordEntity(EntityBase):
    def __init__(self, name=None ):
        super(WordEntity, self).__init__()
        self.Word=name;
        if len(wordlib.keys())==0 :
            initwordlib('libs/wordlib.txt');

    def RebuildEntity(self):
        if wordlib is None:
            print 'please init word lib';
        words=[];
        for r in wordlib:
            if r.startswith(self.Word):
                for w in wordlib[r]:
                    words.append(w);

        self.Re= tnpy.RegexEntity('|'.join(words));
        self.Re.RebuildEntity();
        self.Re.Core=self.Core;
    def RewriteItem(self, input):
        return input

    def MatchItem(self, input, start, muststart, end,mode=None):
        return self.Re.MatchItem(input,start,muststart,end,mode);