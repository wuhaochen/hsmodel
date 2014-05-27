#!/usr/bin/python

import random
import sys
import numpy

N = []
E = []
G = []
S = []

def distance1(nodei,nodej,dim):
    sqr = 0
    for i in range(dim):
        sqr += pow((nodei[i]-nodej[i]),2)
    return pow(sqr,0.5)

def distance(nodei,nodej,dim):
    return numpy.linalg.norm(numpy.array(nodei)-numpy.array(nodej))

def genodes(n,adim,bdim):
    for i in range(n):
        node = {}
        node['id'] = i
        node['a'] = []
        node['b'] = []
        for j in range(adim):
            node['a'].append(random.uniform(0,1))
        for j in range(bdim):
            node['b'].append(random.uniform(0,1))
        N.append(node)

def writenodes(fname='nodes.py'):
    with open(fname,'w') as f:
        f.write("N="+str(N))

def genedges(alpha,beta,adim,bdim):
    for nodei in N:
        for nodej in N:
            diff = distance(nodei['a'][0:adim],nodej['a'][0:adim],adim)
            if diff == 0:
                diff = 0.0000000001
            payoff = alpha/diff
            cost = beta*distance(nodei['b'][0:bdim],nodej['b'][0:bdim],bdim)
            util = payoff - cost
            if util > 0:
                E.append([nodei['id'],nodej['id']])

def writeedges(fname='edges.py'):
    with open(fname,'w') as f:
        f.write("E="+str(E))

def build_adjlist():
    for edge in E:
        if edge[0]!=edge[1]:
            if not G[edge[0]]:
                G[edge[0]] = {}
            if not G[edge[1]]:
                G[edge[1]] = {}
            if not G[edge[0]].has_key(edge[1]):
                G[edge[0]][edge[1]] = True
            if not G[edge[1]].has_key(edge[0]):
                G[edge[1]][edge[0]] = True

def contagion_thr(S,value):
    S_ = S
    for i in range(len(G)):
        thr = abs(N[i]['a'][0]-value)
        total_neighbor = len(G[i])
        infected_neighbor = 0
        for neighbor in G[i]:
            if S[neighbor]:
                infected_neighbor += 1
        if infected_neighbor/total_neighbor >= thr:
            S_[i] = True
    S = S_

def contagion_prob(S,value):    
    S_ = S
    for i in range(len(G)):
        if S[i]:
            for neighbor in G[i]:
                prob = 1-(abs(N[i]['a'][0]-value))
                dice = random.uniform(0,1)
                if dice <= prob:
                    S_[neighbor] = True
    S = S_

def count_infected():
    count = 0
    for status in S:
        if status:
            count += 1
    return count

def write2pfile(fname='output.net'):
    with open(fname,'w') as f:
        f.write("*vertices " +str(len(N))+"\n")
        for node in N:
            f.write(str(node['id']+1)+" \"" + str(node['a']) + str(node['b']) +"\"\n")
            
        f.write("*edges\n")
        for edge in E:
            f.write(str(edge[0]+1)+" "+str(edge[1]+1)+"\n")

def write2gfile(fname='output.gexf'):
    with open(fname,'w') as f:
        f.write("<gexf xmlns:viz=\"http:///www.gexf.net/1.1draft/viz\" xmlns=\"http://www.gexf.net/1.1draft\" version=\"1.1\">\n")
        f.write("\t<graph defaultedgetype=\"undirected\" idtype=\"string\" type=\"static\">\n")
        f.write("\t\t<attributes class=\"node\" mode=\"static\">\n")
        f.write("\t\t\t<attribute id=\"attr\" title=\"Attr\" type=\"string\"/>\n")
        f.write("\t\t\t<attribute id=\"latitude\" title=\"latitude\" type=\"double\"/>\n")
        f.write("\t\t\t<attribute id=\"longitude\" title=\"longitude\" type=\"double\"/>\n")
        f.write("\t\t</attributes>\n")
        
        f.write("\t\t<nodes count=\""+str(len(N))+"\">\n")
        for node in N:
            f.write("\t\t\t<node id=\""+str(node['id'])+"\">\n")
            f.write("\t\t\t\t<attvalues>\n")
            f.write("\t\t\t\t\t<attvalue for=\"attr\" value=\""+str(node['a'])+"\"/>\n")
            f.write("\t\t\t\t\t<attvalue for=\"latitude\" value=\""+str(node['b'][0])+"\"/>\n")
            f.write("\t\t\t\t\t<attvalue for=\"longitude\" value=\""+str(node['b'][1])+"\"/>\n")
            f.write("\t\t\t\t</attvalues>\n")
            f.write("\t\t\t</node>\n")
        f.write("\t\t</nodes>\n")

        f.write("\t\t<edges count=\""+str(len(E))+"\">\n")
        counter = 0
        for edge in E:
            f.write("\t\t\t<edge id=\""+str(counter)+"\" source=\""+str(edge[0])+"\" target=\""+str(edge[1])+"\"/>\n")
            counter += 1
        f.write("\t\t</edges>\n")

        f.write("\t</graph>")
        f.write("</gexf>")

def main(argv,alpha=0.1,beta=1,n=5000,adim=50,bdim=2,fname=''):
    #genodes(n,adim,bdim)
    #genedges(alpha,beta,adim,bdim)

    if fname == '':
        fname = 'n'+str(n)+'a'+str(alpha)+'b'+str(beta)+'u.gexf'

    #write2gfile(fname)

if __name__ == "__main__":
    main(sys.argv[1:])
