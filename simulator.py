from component import component
with open("input/1.txt") as file: 
   data = file.read()
data = data.split('\n')
h = float(data[0])
itterations = int(data[1])
circuitComponents =[]
n = 0 # number of nodes
m = 0 # number of independent voltage sources
nodes = set()
for i in range (2,len(data)-1):
    print(data[i])
    data [i] = data[i].split()
    c = component(data[i][0],data[i][1],data[i][2],data[i][3],data[i][4])
    nodes.add(data[i][1])
    nodes.add(data[i][2])
    circuitComponents.append(c)
n = len(nodes) - 1
