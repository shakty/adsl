import pandas as pd
import numpy as np
import math
import sys
import networkit as nk
import warnings
import optparse
from collections import defaultdict
from threading import Thread
import time
from multiprocessing import Process

#from numba import jit, cuda

def getEdgeQuadranglesMap(graph,edgeresult):
    if (edgeresult!= None):
        mp=dict()
        #print(graph.numberOfEdges())
        for ec in graph.iterEdges():
            #print(ec)
            mp[ec]=edgeresult[graph.edgeId(ec[0],ec[1])]
        return mp
    return None

def reverseOrder(permut):
    for i in range(len(permut)//2):
        mirr=len(permut)-1-i
        t=permut[mirr]
        permut[mirr]=permut[i]
        permut[i]=t

def getThresholdForNumEdges(values,numEdges):
        threshold = 0
        count = 0
        for i in range(len(values)-1):
            count+=1
            threshold=values[i]
            if (count >= numEdges and values[i + 1] != values[i]):
                break
        return threshold 

def make_set(vertice,parent,rank):
    parent[vertice] = vertice
    rank[vertice] = 0

def find(vertice,parent):
    if parent[vertice] != vertice:
        parent[vertice] = find(parent[vertice],parent)
    return parent[vertice]

def union(vertice1, vertice2,parent,rank):
    root1 = find(vertice1,parent)
    root2 = find(vertice2,parent)
    if root1 != root2:
        if rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root1] = root2
        if rank[root1] == rank[root2]:
            rank[root2] += 1 

def func(data,method,multiedges,connectivity,threshold,df,prune,outputfile,verbose):

    #mapping nodes
    node=dict()
    c=0
    for i in data:
        if(i[0] not in node.keys() ):
           node[i[0]]=c
           c+=1   
        if(i[1] not in node.keys() ):
           node[i[1]]=c
           c+=1   
    #print(len(node.keys()))
    inv_map = {v: k for k, v in node.items()}
    df1=df.copy(deep=True)
    df=df.applymap(lambda s: node.get(s) if s in node else s)
    #print(len(df))
    data=df.values.tolist()
    #print(data)

    #initialize graph
    G=nk.graph.Graph(len(node.keys()))

    #adding edges
    for i in range(len(data)):
        G.addEdge(data[i][0],data[i][1]) 

    
    if(multiedges=="no"):
        t= time.time()
        G.removeMultiEdges()
        if(verbose=="yes"):
            print("removing multiedges")
            print("--- %s seconds ---" % (time.time() - t))

    #removing self loops
    G.removeSelfLoops()
    

    #indexing the edges
    G.indexEdges()
    
    #normalized quadrangle scores for edges
    if(method =="quadrilateral"): 
        t= time.time()
        edgeResult1=nk.sparsification.QuadrilateralSimmelianSparsifier().scores(G)
        if(verbose=="yes"):
           print("Quadrangle score")
           print("--- %s seconds ---" % (time.time() - t))
           

    else:
        t= time.time()
        edgeResult1=nk.sparsification.TriangleSparsifier().scores(G)
        if(verbose=="yes"):
           print("Triangle score")
           print("--- %s seconds ---" % (time.time() - t))
           

    #creating map for edges and nodes
    #print(edgeResult1)
    edgeResult=getEdgeQuadranglesMap(G,edgeResult1)
    
    #finding threshold
    mpercentage=threshold
    values=list(edgeResult.values())
    values=np.array(values)
    values=np.sort(values)
    reverseOrder(values)
    numEdges = mpercentage * G.numberOfEdges()
    threshold = getThresholdForNumEdges(values, numEdges)
    #print(threshold)
    unmst=dict()
    for i in G.iterEdges():
        unmst[i]=False
    t = time.time()
    if(connectivity=="maintain"):
        z2=[]
        z2=np.array(z2)
        for e,v in edgeResult.items():
            np.append(z2,[v,e[0],e[1]])
        z2=-np.sort(-z2)
        parent = dict()
        rank = dict()
        for i in G.iterNodes():
            make_set(i,parent,rank)

        #B=[]
        eu=[]
        #eu=np.array(eu)
        i=0
        #construction of the union of all maximum spanning tree
        #print('spanning tree construction')
        #print(z2)
        for k in z2:
            #print(k)
            M=[]
            M=np.array(M)
            elarge=[]
            elarge=np.array(elarge)
            #print(len(z2))
            while(i < len(z2)):
                if z2[i][0]==k[0]:
                    np.append(elarge,[z2[i][1],z2[i][2]])
                    i=i+1
                    t8=i
                else:
                    i=len(z2)
            i=t8
            for ll in elarge:
                if (find(ll[0],parent)!=find(ll[1],parent)):
                    np.append(M,ll)
            for kk in M:
                union(kk[0], kk[1],parent,rank)
            eu.extend(M)
            #B.append(elarge)


        for i in G.iterEdges():
            val=[i[0],i[1]]
            if(eu.count(val)):
                unmst[i]=True
    if(verbose=="yes"):
       print("connectivity")
       print("--- %s seconds ---" % (time.time() - t)) 
    #unmst=getEdgeQuadranglesMap(G,unmst)
    #backbone checking
    backbone=dict()
    for k, v in edgeResult.items():
        if(v>=threshold):
          backbone[k]=True
        elif(unmst[k]):
          backbone[k]=True
        else:
          backbone[k]=False
    #storing in a csv file
    t=time.time()
    col5=[]
    col6=[]
    #col6=np.array(col6,dtype="bool")
    ind1=df1.columns[0]
    ind2=df1.columns[1]
    #print(edgeResult)
    for index,row in df1.iterrows():
        #print(row[0],row[1])
        key=(node[row[ind1]],node[row[ind2]])
        key1=(node[row[ind2]],node[row[ind1]])
        #print(key,key1)
        if(key1 in edgeResult.keys()): 
           col5.append(edgeResult[key1])
           col6.append(backbone[key1])
        elif(node[row[ind1]]==node[row[ind2]]):
             col5.append(1)
             col6.append(False)
        else: 
            col5.append(edgeResult[key])
            col6.append(backbone[key])
    #print(col5,col6)
    df1["redundancy (quadrilateral)"]=pd.Series(col5)
    df1["backbone"]=pd.Series(col6)
    
    if(prune=="yes"):
        if(verbose=="yes"):
           print("pruning")
        df1 = df1[df1['backbone'] == True]
    if(verbose=="yes"):
       print("saving file")
       print("--- %s seconds ---" % (time.time() - t))     
    df1.to_csv(outputfile,index=False)

if __name__ == "__main__":
    start_time = time.time()
    warnings.filterwarnings("ignore")
    parser = optparse.OptionParser()
    parser.add_option('--edgelist', action="store", dest="data", default="input.csv", type="string")
    parser.add_option('--method', action="store", dest="method",choices=("triadic","quadrilateral"), default="quadrilateral")
    parser.add_option('--threshold', action="store", dest="mthreshold", default="0.2", type="string")
    parser.add_option('--multiedges', action="store", dest="multiedges",choices=("yes","no"),default="no")
    parser.add_option('--connectivity', action="store", dest="connectivity", choices=("maintain","ignore"),default="maintain")
    parser.add_option('--prune', action="store", dest="prune", choices=("yes","no"),default="no")
    parser.add_option('--outputlist', action="store", dest="output", default="backbone.csv", type="string")
    parser.add_option('--verbose', action="store", dest="verbose",choices=("yes","no"), default="no")
    options, args = parser.parse_args()
    
    path = options.data
    df=pd.read_csv(path)
    outputfile=options.output
    data=df.values.tolist()
    method=options.method
    multiedges=options.multiedges
    connectivity=options.connectivity
    prune=options.prune
    verbose=options.verbose
    threshold=float(options.mthreshold)
    t = Thread(target=func, args=(data,method,multiedges,connectivity,threshold,df,prune,outputfile,verbose,))
    #p = Process(target=func, args=(data,method,multiedges,connectivity,threshold,df,))
    #func(data,method,multiedges,connectivity,threshold,df)
    t.start()
    t.join()
    if(verbose=="yes"):
       print("--- Total time taken: %s ---" % (time.time() - start_time))