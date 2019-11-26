class node:
    def __init__(self,name):
        self.name=name
        self.connected = [] # components connected

    def addComponent(self,component):
        self.connected.append(component)

    def getResistors(self):
        arr =[]
        for i in range (len(self.connected)):
            if self.connected[i].ctype == 'R':
                arr.append(self.connected[i])
        return arr