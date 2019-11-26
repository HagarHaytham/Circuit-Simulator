class component:
    def __init__(self,ctype,node1,node2,value,initial_value):
        self.ctype = ctype
        self.node1 = node1
        self.node2 = node2
        self.value = float(value)
        self.initial_value = float(initial_value)

    def __str__(self):
        return self.ctype+ " "+ self.node1 +" "+ self.node2+" "+ str(self.value)+" "+ str(self. initial_value)