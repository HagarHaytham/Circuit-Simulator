from component import component
from node import node
import numpy as np

infile ="testcases/2.txt"
with open(infile)as file:
    data = file.read()
data = data.split('\n')

h = float(data[0])
iterations = int(data[1])
circuitComponents =[]
n = 0 # number of nodes
m = 0 # number of independent voltage sources
nodesNames = set()

for i in range (2,len(data)-1):
    data [i] = data[i].split()
    c = component(data[i][0],data[i][1],data[i][2],data[i][3],data[i][4])
    if data[i][0] == 'Vsrc':
        m+=1
    # An inductance 
    if data[i][0] == 'I':
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
G = np.zeros((n,n))

#Computing Diagonal Elements.
for i in range (len(nodes)):
    if nodes[i].name =='V0':
        continue
    pos = int(nodes[i].number)-1
    r = nodes[i].getResistors()
    for j in range(len(r)):
        G[pos][pos]+= 1/r[j].value
    c = nodes[i].getCapacitors()
    for j in range(len(c)):
        G[pos][pos]+= c[j].value/h

#Computing Off Diagonal Elements.
for i in range (len(nodes)):
    if nodes[i].name =='V0':
        continue
    pos = nodes[i].number-1
    r = nodes[i].getResistors()
    c = nodes[i].getCapacitors()

    #### TODO :: ADD C's here.
    for j in range(len(r)):
        if int(r[j].node1[1]) > nodes[i].number:
            G[nodes[i].number-1][int(r[j].node1[1])-1] += -1/r[j].value
            G[int(r[j].node1[1])-1][nodes[i].number-1] += -1/r[j].value
        elif int(r[j].node2[1]) > nodes[i].number:
            G[nodes[i].number-1][int(r[j].node2[1])-1] += -1/r[j].value
            G[int(r[j].node2[1])-1][nodes[i].number-1] += -1/r[j].value
    for j in range(len(c)):
        if int(c[j].node1[1]) > nodes[i].number:
            G[nodes[i].number-1][int(c[j].node1[1])-1] += -c[j].value/h
            G[int(c[j].node1[1])-1][nodes[i].number-1] += -c[j].value/h
        elif int(c[j].node2[1]) > nodes[i].number:
            G[nodes[i].number-1][int(c[j].node2[1])-1] += -c[j].value/h
            G[int(c[j].node2[1])-1][nodes[i].number-1] += -c[j].value/h

print(n,m)
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
for i in range(len(circuitComponents)):
    if circuitComponents[i].ctype == 'I':
        nodeNum1 = int(circuitComponents[i].node1[1]) -1
        nodeNum2 = int(circuitComponents[i].node2[1]) -1
        if nodeNum1 >=0:
            B[nodeNum1][vsrc] = 1
        if nodeNum2 >=0:
            B[nodeNum2][vsrc] = -1
        vsrc+=1

C = B.transpose()
D = np.zeros((m,m))
j = 0
for i in range(len(circuitComponents)):
    if circuitComponents[i].ctype == 'Vsrc':
        D[j][j] = 0
        j+=1
    
for i in range(len(circuitComponents)):
    if circuitComponents[i].ctype == 'I':
        D[j][j] = -1*circuitComponents[i].value/h
        j+=1
  
A1 = np.block([[G],[C]])
A2 = np.block([[B],[D]])
A = np.block([A1,A2])
#Constructing Z vector, without C,I terms.
I = np.zeros((n,1))
E = np.zeros((m,1))
vsrc = 0
for i in range(len(circuitComponents)):
    if circuitComponents[i].ctype == 'Vsrc':
        E[vsrc] = circuitComponents[i].value
        vsrc +=1
    elif circuitComponents[i].ctype == 'Isrc':
        # get the node position
        node1 = int(circuitComponents[i].node1[1]) -1
        node2 = int(circuitComponents[i].node2[1]) -1
        if node1 >=0:
            I[node1] += circuitComponents[i].value
        if node2 >=0:
            I[node2] += circuitComponents[i].value

Z = np.block([[I],[E]])


def calculate_It_Z(V_init,I_init):
    tmp_1 = np.zeros((n,1))
    tmp_2 = np.zeros((m,1))
    vsrc = 0
    for i in range(len(circuitComponents)):
        if circuitComponents[i].ctype == 'Vsrc':
            tmp_2[vsrc] = 0
            vsrc += 1
    for i in range(len(circuitComponents)):
        if circuitComponents[i].ctype == 'I':
            tmp_2[vsrc] = -1*circuitComponents[i].value/h*I_init
            vsrc += 1
    for i in range(len(circuitComponents)):   
        if circuitComponents[i].ctype == 'C':
            node1 = int(circuitComponents[i].node1[1]) -1
            node2 = int(circuitComponents[i].node2[1]) -1
            if node1 >=0:
                tmp_1[node1] += ((circuitComponents[i].value/h)*V_Init)
            if node2 >=0:
                tmp_1[node2] -= ((circuitComponents[i].value/h)*V_Init)
        
    It = np.block([[tmp_1],[tmp_2]])
    return It



print(A)
print(Z)
print(calculate_It_Z(0,0))
A_inv = np.linalg.inv(A)
for i in range(iterations):
    X = np.matmul(A_inv,Z+calculate_It_Z(0,0))
    print(X)