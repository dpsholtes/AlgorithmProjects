#Code by Dylan Sholtes
#Binary Search Tree and Red-Black Tree searching
#timing module
import time
import decimal
#Node Class
class Node():
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None

class BinarySearchTree():
    #On creation of the tree, the root will be declared as none
    def __init__(self):
        self.root = None
    
    def insert(self, z):
        y = None
        x = self.root
        while x != None:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
    def treeSearch(self, x, k):
        if x == None or k == x.key:
            return x
        if k < x.key:
            return self.treeSearch(x.left, k)
        else:
            return self.treeSearch(x.right, k)
    def iterativeTreeSearch(self, x, k):
        while x != None and k != x.key:
            if k < x.key:
                x = x.left
            else:
                x = x.right
        return x
def openFiletoArray(filename):
        f = open(filename)
        wordList = f.read().split()
        f.close()
        return wordList
def createNodeList(wordList):
    nodeList = []
    for word in wordList:
        nodeList.append(Node(word))
    return nodeList
#Red-Black Tree node differs from a BST node, as a color is required, it must be either red or black, with the root being black.
class RBNode():
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.color = "Red"
class RBT():
    #Creating a TNIL node initialized to black color, leaf nodes of the tree will point to TNIL
    def __init__(self):
        self.TNIL = RBNode(0)
        self.TNIL.color = "Black"
        self.root = self.TNIL
    #Red Black Tree Functions go here
    def leftRotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.TNIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
    def rightRotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.TNIL:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
    def RBInsert(self, z):
        y = self.TNIL
        x = self.root
        while x != self.TNIL:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if  y == self.TNIL:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = self.TNIL
        z.right  = self.TNIL
        z.color = "Red"
        self.RBInsertFixup(z)
    def RBInsertFixup(self, z):
        while z.parent.color == "Red":
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == "Red":
                    z.parent.color = "Black"
                    y.color = "Black"
                    z.parent.parent.color = "Red"
                    z = z.parent.parent
                else:
                    if z  == z.parent.right:
                        z = z.parent
                        self.leftRotate(z)
                    z.parent.color = "Black"
                    z.parent.parent.color = "Red"
                    self.rightRotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == "Red":
                    z.parent.color = "Black"
                    y.color = "Black"
                    z.parent.parent.color = "Red"
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.rightRotate(z)
                    z.parent.color = "Black"
                    z.parent.parent.color = "Red"
                    self.leftRotate(z.parent.parent)
        self.root.color = "Black"
    def RBTreeSearch(self, x, k):
        if x == None or k == x.key:
            return x
        if k < x.key:
            return self.RBTreeSearch(x.left, k)
        else:
            return self.RBTreeSearch(x.right, k)
    def iterativeRBTreeSearch(self, x, k):
        while x != None and k != x.key:
            if k < x.key:
                x = x.left
            else:
                x = x.right
        return x
    


def createRBNodeList(wordList):
    nodeList = []
    for word in wordList:
        nodeList.append(RBNode(word))
    return nodeList
   
if __name__ == "__main__":
    filename = input("Enter the name of the file you are searching through, Ex. perm15K.txt: ")
    wordList = openFiletoArray(filename)
    userChoice = False
    while (userChoice == False):
        choice = input("Enter the data structure you would like to use, BST for Binary Search Tree or RB for Red-Black Tree: ")
        if choice == "BST" or choice == "bst":
            userChoice = True
            tree = BinarySearchTree()
            nodeList = createNodeList(wordList)
            start = time.time()
            for node in nodeList:
                tree.insert(node)
            end = time.time()
            BSTCreationTime = end - start
            print("Binary Search Tree took", BSTCreationTime, "seconds to create.")
            searchFor = input("Enter the word you are searching for: ")
            print("Recursive Tree Search:")
            x = tree.root
            start = time.time()
            item = tree.treeSearch(x, searchFor)
            end = time.time()
            BSTRecursiveTime = end - start
            print("Recursive Binary Search took", decimal.Decimal(BSTRecursiveTime), "seconds.")
            if item != None:
                print("Word", searchFor , "successfully found.")
            else:
                print("Word", searchFor, "not found.")
            print("Iterative Tree Search:")
            start = time.time()
            x = tree.root
            item2 = tree.iterativeTreeSearch(x, searchFor)
            end = time.time()
            BSTIterativeTime = end - start
            print("Iterative Binary Search took", decimal.Decimal(BSTIterativeTime), "seconds.")
            if item != None:
                print("Word", searchFor, "successfully found.")
            else:
                print("Word", searchFor, "not found.")
        elif choice == "RB" or choice == "rb":
            userChoice = True
            tree = RBT()
            nodeList = createRBNodeList(wordList)
            start = time.time()
            for node in nodeList:
                tree.RBInsert(node)
            end = time.time()
            RBCreationTime = end - start
            print("Red-Black Tree took", RBCreationTime, "seconds to build.")
            searchFor = input("Enter the word you are searching for: ")
            print("Recursive Red-Black Tree Search:")
            x = tree.root
            start = time.time()
            item = tree.RBTreeSearch(x, searchFor)
            if item != None:
                print("Word", searchFor, "successfully found.")
            else:
                print("Word", searchFor, "not found.")
            end = time.time()
            RBTreeSearchTime = end - start
            print("Recursive Red Black Tree Search took", decimal.Decimal(RBTreeSearchTime), "seconds.")
            print("Iterative Tree Search:")
            start = time.time()
            x = tree.root
            item2 = tree.iterativeRBTreeSearch(x, searchFor)
            end = time.time()
            RBIterativeTime = end - start
            print("Iterative Red Black Tree Search took", decimal.Decimal(RBIterativeTime), "seconds." )
            if item != None:
                print("Word", searchFor, "successfully found.")
            else:
                print("Word", searchFor, "not found.")
        else:
            print("Please enter in BST or RB to continue")
    
