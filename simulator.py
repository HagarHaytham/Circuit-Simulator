from component import component
from node import node

import numpy as np
infile="4.txt"
with open("input/"+infile) as file: 
   data = file.read()
data = data.split('\n')

h = float(data[0])
itterations = int(data[1])
circuitComponents =[]
n = 0 # number of nodes
m = 0 # number of independent voltage sources
nodesNames = set()

# extract circuit components from file
for i in range (2,len(data)-1):
    print(data[i])
    data [i] = data[i].split()
    c = component(data[i][0],data[i][1],data[i][2],data[i][3],data[i][4])
    if data[i][0] == 'Vsrc':
        m+=1
    nodesNames.add(data[i][1])
    nodesNames.add(data[i][2])
    circuitComponents.append(c)
n = len(nodesNames) - 1 # without ground
nodes = []
for name in nodesNames:
    nodes.append(node(name))

# add connected components to each node
for i in range (len(nodes)):
    for j in range (len(circuitComponents)):
        if circuitComponents[j].node1 == nodes[i].name:
            nodes[i].addComponent(circuitComponents[j])
        elif circuitComponents[j].node2 == nodes[i].name:
            nodes[i].addComponent(circuitComponents[j])

l= nodes[0].getResistors()
G = np.zeros((n,n))
# first diagonal elements of G
for i in range (len(nodes)):
    if nodes[i].name =='V0':
        continue
    pos = int(nodes[i].number)-1
    r = nodes[i].getResistors()
    for j in range(len(r)):
        G[pos][pos]+= 1/r[j].value

# second off-diagonal elements of G
for i in range (len(nodes)):
    if nodes[i].name =='V0':
        continue
    pos = nodes[i].number-1
    r = nodes[i].getResistors()
    for j in range(len(r)):
        if int(r[j].node1[1]) > nodes[i].number:
            G[nodes[i].number-1][int(r[j].node1[1])-1] += -1/r[j].value
            G[int(r[j].node1[1])-1][nodes[i].number-1] += -1/r[j].value
        elif int(r[j].node2[1]) > nodes[i].number:
            G[nodes[i].number-1][int(r[j].node2[1])-1] += -1/r[j].value
            G[int(r[j].node2[1])-1][nodes[i].number-1] += -1/r[j].value

# compute B
B = np.zeros((n,m))
vsrc = 0
for i in range(len(circuitComponents)):
    if circuitComponents[i].ctype == 'Vsrc':
        nodeNum1 = int(circuitComponents[i].node1[1]) -1
        nodeNum2 = int(circuitComponents[i].node2[1]) -1
        if nodeNum1 >=0:
            B[nodeNum1][vsrc] = 1
        if nodeNum2 >=0:
            B[nodeNum2][vsrc] = -1
        vsrc+=1
# compute C and D
C = B.transpose()
D = np.zeros((m,m)) # ???
# construct A
A1 = np.block([[G],[C]])
A2 = np.block([[B],[D]])
A = np.block([A1,A2])
print(A)

I = np.zeros((n,1))
E = np.zeros((m,1))
vsrc = 0
for i in range(len(circuitComponents)):
    if circuitComponents[i].ctype == 'Vsrc':
        E[vsrc] = circuitComponents[i].value
    elif circuitComponents[i].ctype == 'Isrc':
        # get the node position
        node1 = int(circuitComponents[i].node1[1]) -1
        node2 = int(circuitComponents[i].node2[1]) -1
        if node1 >=0:
            I[node1] += circuitComponents[i].value
        if node2 >=0:
            I[node2] += circuitComponents[i].value
#construct Z 
Z = np.block([[I],[E]])
print(Z)

A_inv = np.linalg.inv(A)
print(A_inv)
X = np.matmul(A_inv,Z)
print(X)

nodesNum =[]
for x in nodesNames:
    nodesNum.append(int(x[1]))

nodesNum.sort()
with open ('myoutput/'+infile,'w') as outfile:
    for i in range(1,len(nodesNum)):
        outfile.write('V'+str(nodesNum[i])+'\n')
        outfile.write(str(h)+" "+str(X[i-1][0])+'\n\n')
    for i in range (n,n+m):
        outfile.write('I_Vsrc'+str(i-n)+'\n')
        outfile.write(str(h)+" "+str(X[i][0])+'\n\n')


#Calculating The modified G matrix to consider  