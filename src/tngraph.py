__author__ = 'zhaoyiming-laptop'
import pygraphviz as pgv
import os;
from src.tnpy import StringEntity as SE, RegexEntity as RE, TableEntity as TE, SequenceEntity as SQE, RepeatEntity as RPE, \
    EntityBase
os.environ["PATH"]= r'D:\Program Files\graphviz-2.38\release\bin;'+os.environ["PATH"];
# strict (no parallel edges)
# digraph
# with attribute rankdir set to 'LR'

def addNode(A,entity,nodes):
    nodeid= id(entity);
    name= str(entity);
    if nodeid not in nodes:
        A.add_node(name);
        nodes[nodeid]=entity;
    if isinstance(entity, SQE):
        for child in entity.MatchEntities:
            addNode(A,child,nodes);
            A.add_edge(name,str(child));
        for child in entity.RewriteEntities:
            addNode(A,child,nodes);
            A.add_edge(name,str(child));
    elif isinstance(entity, TE):
        for child in entity.Tables:
            addNode(A,child,nodes);
            A.add_edge(name,str(child));



    A.add_node(entity)
def buildGraph(tn,entityname):
    A=pgv.AGraph(directed=True,strict=True)
    entities=tn.Entities;
    entity= entities[entityname];
    nodes={};
    addNode(A,entity,nodes);
    A.graph_attr['epsilon']='0.001'
    print (A.string()) # print dot file to standard output
    A.write('foo.dot')
    A.layout('dot') # layout with dot
    A.draw('foo.png') # write to file

