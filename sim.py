#!/usr/bin/python

import random
import sys
import numpy

N = []
E = []

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

def genedges(alpha,beta,adim,bdim):
    for nodei in N:
        for nodej in N:
            diff = distance(nodei['a'],nodej['a'],adim)
            if diff == 0:
                diff = 0.0000000001
            payoff = alpha/diff
            cost = beta*distance(nodei['b'],nodej['b'],bdim)
            util = payoff - cost
            if util > 0:
                E.append([nodei['id'],nodej['id']])

def write2pfile(fname=''):
    with open(fname,'w') as f:
        f.write("*vertices " +str(len(N))+"\n")
        for node in N:
            f.write(str(node['id']+1)+" \"" + str(node['a']) + str(node['b']) +"\"\n")
            
        f.write("*edges\n")
        for edge in E:
            f.write(str(edge[0]+1)+" "+str(edge[1]+1)+"\n")

def write2gfile(fname=''):
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
    genodes(n,adim,bdim)
    genedges(alpha,beta,adim,bdim)

    if fname == '':
        fname = 'n'+str(n)+'a'+str(alpha)+'b'+str(beta)+'u.gexf'

    write2gfile(fname)

if __name__ == "__main__":
    main(sys.argv[1:])
