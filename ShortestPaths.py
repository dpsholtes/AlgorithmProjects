#Code by Dylan Sholtes
from collections import defaultdict, deque
import math
class Graph():
    def __init__(self):
        self.graph = defaultdict(list)
        self.vertices = 0
        self.cycleExists = False
        self.dist = []
        self.shortestpath = []
        self.topoOrder = deque()
        self.topoList = []


    def addEdgesfromFile(self, filename):
        try:
            with open(filename) as f:
                largestVertex = 0
                for line in f:
                    templist = []
                    templist = line.split(":")
                    temp2 = []
                    temp2 = line.split()
                    temp2 = temp2[1:]
                    j = 1
                    for i in range(0, len(temp2), 2):
                        vertex1 = int(templist[0])
                        vertex2 =  int(temp2[i])
                        weight = int(temp2[j])
                        #this determines the largest vertex, to determine the total number of vertices
                        if int(templist[0]) > largestVertex:
                            largestVertex = int(templist[0])
                        if int(temp2[i]) > largestVertex:
                            largestVertex = int(temp2[i])
                        j = j + 2
                        self.graph[vertex1].append((vertex2, weight))
                f.close()
                self.vertices = largestVertex
                self.shortestpath = [None] * self.vertices
        except FileNotFoundError:
            print("File was not found, Please try again.")
            exit(0)
    def isVertex(self, vertex):
        if vertex <= self.vertices:
            return True
        else:
            return False
    def dequeToList(self):
        while (len(self.topoOrder) > 0):
            self.topoList.append(self.topoOrder.popleft())

    def DFS(self):
        color = ["White"] * (self.vertices + 1)
        for i in range(1 , self.vertices + 1):
            if color[i] == "White":
                self.DFSVisit(i, color)
        if self.cycleExists == False:
            self.dequeToList()
            return True
        elif self.cycleExists == True:
            return False
    def DFSVisit(self, u, color):
        color[u] = "Gray"
        for v in self.graph[u]:
            if color[v[0]] == "White":
                self.DFSVisit(v[0], color)
            if color[v[0]] == "Gray":
                self.cycleExists = True
        color[u] = "Black"
        self.topoOrder.appendleft(u)
    
    def checkEdgeWeights(self):
        for i in range(1, self.vertices + 1):
            for w in self.graph[i]:
                if w[1] < 0:
                    return False
        return True
    def initializeSingleSource(self, source):
        self.dist = [math.inf] * (self.vertices + 1)
        self.dist[source] = 0
    
    def relax(self, u, v, w):
        if self.dist[u] != math.inf and self.dist[u] + w < self.dist[v]:
            self.dist[v] = self.dist[u] + w
            self.shortestpath[u] = v
    def BellmanFord(self, source, dest):
        self.initializeSingleSource(source)
        for i in range(1, self.vertices - 1):
            #nested loop still runs VE time, as it only loops through edges in the graph
            for e in self.graph:
                for v in self.graph[e]:
                    self.relax(e, v[0], v[1])
        for e in self.graph:
                for v in self.graph[e]:
                    if self.dist[e] != math.inf and self.dist[e] + v[1] < self.dist[v[0]]:
                        print("Graph contains negative weight cycle")
                        exit(0)
        self.shortestPathPrint(source, dest)

    def shortestPathPrint(self, source, dest):
        print("Shortest Path")
        print(source)
        print(self.shortestpath[source])
        i = self.shortestpath[source]
        while(i != dest):
            print(self.shortestpath[i])
            i = self.shortestpath[i]
        print("Total Distance to Destination")
        print(self.dist[dest])

    def dagSP(self, source, dest):
        self.initializeSingleSource(source)
        for u in self.topoList:
            for v in self.graph[u]:
                self.relax(u, v[0], v[1])
        self.shortestPathPrint(source, dest)
    
    def dijkstraSP(self, source, dest):
        self.initializeSingleSource(source)
        minHeap = Heap()
        #null position for zeroth vertex
        for v in range(self.vertices + 1):
            minHeap.insert(v, self.dist[v])
        minHeap.positionInHeap[source] = source
        minHeap.decreaseKey(source, self.dist[source])
        while(minHeap.heapsize > 0):
            u = minHeap.extractMin()
            u = u[0]
            for v in self.graph[u]:
                self.relax(u, v[0], v[1])
                if self.dist[u] != math.inf and self.dist[u] + v[1] < self.dist[v[0]]:
                    minHeap.decreaseKey(v, self.dist[v])
        self.shortestPathPrint(source, dest)    



        
class Heap():
    def __init__(self):
        self.heap = []
        self.heapsize = 0
        self.positionInHeap = []
    #modified maxHeapify from project1, changed largest to smallest, modified to base on weights, and added positionInHeap swapping
    def minHeapify(self, i):
        l = 2 * i + 1
        r = 2 * i + 2
        if l <= self.heapsize and self.heap[l][1] < self.heap[i][1]:
            smallest = l
        else:
            smallest = i
        if r <= self.heapsize and self.heap[r][1] < self.heap[smallest][1]:
            smallest = r
        if smallest != i:
            #swap the positions
            self.positionInHeap[self.heap[smallest][0]] = i
            self.positionInHeap[self.heap[i][0]] = smallest
            #swap the nodes
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self.minHeapify(smallest)
    #extract min implementation, takes the smallest
    def extractMin(self):
        root = self.heap[0]
        lastVertex = self.heap[self.heapsize - 1]
        self.heap[0] = lastVertex
        #update position in Heap
        self.positionInHeap[self.heap[0][0]] = 0
        self.positionInHeap[root[0]] = self.heapsize - 1
        self.heapsize -= 1
        self.minHeapify(0)
        return root
    #insert into heap and append into positioninHeap, increases heapsize
    def insert(self, vertex, weight):
        self.heap.append([vertex, weight])
        self.positionInHeap.append(vertex)
        self.heapsize += 1
    #decreaseKey acceses vertex in heap and changes weight, travels up the heap and swaps until heap is a min heap
    def decreaseKey(self, vertex, weight):
        i = self.positionInHeap[vertex]
        self.heap[int(i)][1] = weight
        while i > 0:
            parent = int((i - 1) / 2)
            if self.heap[int(i)][1] > self.heap[int(parent)][1]:
                break
            else:
                self.positionInHeap[self.heap[int(i)][0]] = parent
                self.positionInHeap[self.heap[int(parent)][0]] = i
                self.heap[int(i)], self.heap[int(parent)] = self.heap[int(parent)], self.heap[int(i)]
                i = parent


  
if __name__ == "__main__":
    graph = Graph()
    filename = input("Please enter the name of the file ex. graphin_Fig1.txt: ")
    graph.addEdgesfromFile(filename)
    bellman = False
    dfs = False
    dijkstra = False
    if graph.DFS() == True:
        dfs = True
        print("Graph is a DAG, DAG SP will be used.")
    else:
        if graph.checkEdgeWeights() == True:
            dijkstra = True
            print("Graph is a Non Dag with only postive weights, Dijkstra's will be used.")
        else:
            bellman = True
            print("Graph is a Non Dag with negative edge weights, Bellman Ford will be used.")
    hasSource = False
    while(hasSource == False):
        source = input("Please enter the source vertex: ex. 1   ")
        source = int(source)
        if graph.isVertex(source) == False:
            print("Please enter a valid vertex")
        else:
            hasSource = True
    userChoice = True
    while(userChoice == True):
        destination = input("Please enter a destination node: ex. 2   ")
        destination = int(destination)
        if graph.isVertex(source) == True:
            #perform shortest path here
            if bellman == True:
                graph.BellmanFord(source, destination)
            elif dfs == True:
                graph.dagSP(source, destination)
            elif dijkstra == True:
                graph.dijkstraSP(source, destination)
            choice = ""
            while(choice != "Y"):
                choice = input("Would you like to enter another destination, Y/N  ")
                if choice == "Y":
                    userChoice = True
                elif choice == "N":
                    userChoice = False
                    exit(0)
                else:
                    print("Please enter Y or N")

        else:
            print("Please enter a valid vertex")
    
        
        
