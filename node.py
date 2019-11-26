class node:
    def __init__(self,name):
        self.name=name
        self.number = int(name[1])
        self.connected = [] # components connected

    def addComponent(self,component):
        self.connected.append(component)

    def getResistors(self):
        arr =[]
        for i in range (len(self.connected)):
            if self.connected[i].ctype == 'R':
                arr.append(self.connected[i])
        return arr
    def getCapacitors(self):
        arr = []
        for i in range(len(self.connected)):
            if self.connected[i].ctype == 'C':
                arr.append(self.connected[i])
        return arr
    def getInductors(self):
        arr = []
        for i in range(len(self.connected)):
            if self.connected[i].ctype == 'I':
                arr.append(self.connected[i])
        return arr