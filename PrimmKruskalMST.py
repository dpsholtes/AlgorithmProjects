#code by Dylan Sholtes for Project 4, CS340
import math

class Graph():
    def __init__(self):
        self.graph = []
        self.MST = []
        self.numEdges = 0


    def addEdgesfromFile(self, filename):
        try:
            with open(filename) as f:
                for line in f:
                    templist = []
                    templist = line.split(":")
                    temp2 = []
                    temp2 = line.split()
                    temp2 = temp2[1:]
                    j = 1
                    largestVertex = 0
                    for i in range(0, len(temp2), 2):
                        #this is an edge of the graph, it is a dictionary with 3 values, starting vertex, end vertex, and weight
                        edge = {
                            "vertex1":  int(templist[0]),
                            "vertex2":  int(temp2[i]),
                            "weight" : int(temp2[j])
                        }
                        #this determines the largest vertex, to determine the total number of vertices
                        if int(templist[0]) > largestVertex:
                            largestVertex = int(templist[0])
                        if int(temp2[i]) > largestVertex:
                            largestVertex = int(temp2[i])
                        j = j + 2
                        self.graph.append(edge)
                f.close()
                self.numEdges = len(self.graph)
                self.vertices = largestVertex
        except FileNotFoundError:
            print("File was not found, Please try again.")
            exit(0)
    #merge sort implementation from project 1
    def mergeSort(self, l, r):
        if l < r:
            mid = (r + l) // 2
            self.mergeSort(l, mid)
            self.mergeSort(mid + 1, r)
            self.merge(l, mid, r)

    def merge(self, l, mid, r):
        L = self.graph[l:mid + 1]
        R = self.graph[mid + 1:r + 1]
        infedge = {
            "vertex1": math.inf,
            "vertex2": math.inf,
            "weight" : math.inf,
        }
        L.append(infedge)
        R.append(infedge)
        i = 0
        j = 0
        k = 0
        for k in range(l, r + 1):
            if L[i]["weight"] <= R[j]["weight"]:
                self.graph[k] = L[i]
                i = i + 1    
            else:
                self.graph[k] = R[j]
                j = j + 1
    #FindSet Implementation for Disjoint set
    def FindSet(self, parent, i):
        if parent[i] != i:
            return self.FindSet(parent, parent[i])
        return parent[i]
    #union by depth
    def Union(self, x, y, rank, parent):
        self.Link(self.FindSet(parent, x), self.FindSet(parent, y), rank, parent)
    #Link Implementation for Disjoint set
    def Link(self, x, y, rank, parent):
        if rank[x] > rank[y]:
            parent[y] = x
        else:
            parent[x] = y
            if rank[x] == rank[y]:
                rank[y] = rank[y] + 1
    
    def MSTKruskal(self):
        #holds parents and ranks
        parent = []
        rank = []
        #sort the graph
        self.mergeSort(0, self.numEdges - 1)

        #fill parent and rank
        #add dummy parent and rank for vertex 0, since we are not using a vertex 0
        parent.append(0)
        rank.append(0)
        for x in range(1, self.vertices + 1):
            parent.append(x)
            rank.append(0)
        
        for e in range(self.numEdges):
            u =  self.graph[e]["vertex1"]
            v = self.graph[e]["vertex2"]
            w = self.graph[e]["weight"]
            if self.FindSet(parent, u) != self.FindSet(parent, v):
                edgetoAppend = {
                    "vertex1": u,
                    "vertex2": v,
                    "weight": w
                }
                self.MST.append(edgetoAppend)
                self.Union(u, v, rank, parent)

    def MSTPrim(self):
        #holds weights for vertexes, initialized to infinity, weight for key is updated after being added to MST
        key = []
        minHeap = Heap()
        #append infinity to keys and insert each vertex to min heap. Vertices + 1 to include last vertex
        for vertex in range(0, self.vertices + 1):
            key.append(math.inf)
            minHeap.insert(vertex, key[vertex])
            #add null values to MST for each vertex after zero, since there is no zeroth vertex. 
            if vertex > 0:
                self.MST.append(-1)
        #set key and position of "zeroth vertex" to zero to ensure it gets extracted first
        #it will never pass the loop and will be discarded
        minHeap.positionInHeap[0] = 0
        key[0] = 0
        minHeap.decreaseKey(0, key[0])
        while minHeap.heapsize > 0:
            #indexing variable
            i = 0
            #extract min weight vertex from the heap
            u = minHeap.extractMin()
            #finding where the adjacent vertices are
            for x in range(self.numEdges - 1):
                if self.graph[x]["vertex1"] ==  u[0]:
                    i = x
                    break
            #loop through adjacent vertices, and add to MST
            while(i < self.numEdges and self.graph[i]["vertex1"] == u[0]):
                v = self.graph[i]["vertex2"]
                if minHeap.positionInHeap[v] < minHeap.heapsize and  self.graph[i]["weight"] < key[v]:
                    key[v] = self.graph[i]["weight"]
                    self.MST[v] = u[0]
                    minHeap.decreaseKey(v, key[v])
                i += 1
         
    def kruskalToFile(self):
        f = open("kruskalout.txt", "w")
        for line in self.MST:
            f.write('%d %d\n' % (line["vertex1"], line["vertex2"]))

    def primToFile(self):
        f = open("primout.txt", "w")
        for i in  range(1, self.vertices):
            f.write('%d %d\n' % (i, self.MST[i]))

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
    filename = input("Enter the name of the file that you would like to perform Prims or Kruskals on, ex. graphin_w_ud.txt: ")
    graph.addEdgesfromFile(filename)
    userChoice = False
    while (userChoice == False):
        choice = input("Enter K for Kruksals Algorithm, or P for Prims Algorithm: ")
        if (choice == "K" or choice == "k"):
            userChoice = True
            graph.MSTKruskal()
            graph.kruskalToFile()
        elif (choice == "P" or choice == "p"):
            userChoice = True
            graph.MSTPrim()
            graph.primToFile()
        else:
            print("Please enter a vaild choice, K for Kruskal, P for Prim")

