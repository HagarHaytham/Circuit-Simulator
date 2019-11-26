from component import component
from node import node


with open("input/1.txt") as file: 
   data = file.read()
data = data.split('\n')

h = float(data[0])
itterations = int(data[1])
circuitComponents =[]
n = 0 # number of nodes
m = 0 # number of independent voltage sources
nodesNames = set()

for i in range (2,len(data)-1):
    print(data[i])
    data [i] = data[i].split()
    c = component(data[i][0],data[i][1],data[i][2],data[i][3],data[i][4])
    nodesNames.add(data[i][1])
    nodesNames.add(data[i][2])
    circuitComponents.append(c)
n = len(nodesNames) - 1
nodes = []
for name in nodesNames:
    nodes.append(node(name))

for i in range (len(nodes)):
    for j in range (len(circuitComponents)):
        if circuitComponents[j].node1 == nodes[i].name:
            nodes[i].addComponent(circuitComponents[j])
        elif circuitComponents[j].node2 == nodes[i].name:
            nodes[i].addComponent(circuitComponents[j])

l= nodes[0].getResistors()
