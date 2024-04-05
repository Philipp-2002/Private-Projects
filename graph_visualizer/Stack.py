
class Stack:
    data = []

    def __init__(self):
        self.data = []


    def add(self, element):
        self.data.append(element)

    def removeTop(self):
        self.data = self.data[:len(self.data)-1]
        

    def getTop(self):
        return self.data[len(self.data)-1]

    def getLength(self):
        return len(self.data)
