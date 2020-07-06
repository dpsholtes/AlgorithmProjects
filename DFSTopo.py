from collections import deque, defaultdict


class Graph():
    def __init__(self):
        self.vertices = 0
        self.graph = defaultdict(list)
        self.topoOrder = deque()
        self.cycleExists = False
        self.backEdge = deque()

    def addEdgesfromFile(self, filename):
        with open(filename) as f:
            for line in f:
                templist = []
                templist = line.split(":")
                temp2 = []
                temp2 = line.split()
                temp2 = temp2[1:]
                if len(temp2) == 0:
                    temp2.append(0)
                for i in range(0, len(temp2)):
                    self.graph[int(templist[0])].append(int(temp2[i]))
            f.close()
            self.vertices = len(self.graph)

    
    def DFS(self):
        color = ["White"] * (self.vertices + 1)
        for i in range(1 , self.vertices + 1):
            if color[i] == "White":
                self.DFSVisit(i, color)
        if self.cycleExists == False:
            self.topoSort()
        elif self.cycleExists == True:
            print("Cycle exists, Back Edges occur at:")
            while(len(self.backEdge) > 0):
                print(self.backEdge.popleft())
    def DFSVisit(self, u, color):
        color[u] = "Gray"
        for v in self.graph[u]:
            if color[v] == "White":
                self.DFSVisit(v, color)
            if color[v] == "Gray":
                self.backEdge.appendleft((u, v))
                self.cycleExists = True
        color[u] = "Black"
        self.topoOrder.appendleft(u)
    def topoSort(self):
        self.topoOrder.remove(0)
        print("Topological Order")
        while(len(self.topoOrder) > 0):
            print(self.topoOrder.popleft())

if __name__ == "__main__":
    filename = input("Enter the name of the graph file, ex. graphin-c1.txt:  ")
    graph = Graph()
    graph.addEdgesfromFile(filename)
    print("Graph Created, Performing DFS Topo Sort")
    graph.DFS()




            
        
