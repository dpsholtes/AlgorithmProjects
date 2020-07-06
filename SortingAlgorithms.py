import math
import time
#Code by Dylan Sholtes
#timing variables
istime = 0
mstime = 0
bhtime = 0
hstime = 0
def insertionSorttoFile(sortList, filename):
    f = open(filename.replace("perm", "IS"), "w")
    for s in sortList:
        f.write('%s\n' % s)
def mergeSorttoFile(sortList, filename):
    f = open(filename.replace("perm", "MS"), "w")
    for s in sortList:
        f.write('%s\n' % s)
    f.close()
def heapSorttoFile(sortList, filename):
    f = open(filename.replace("perm", "HS"), "w")
    for s in sortList:
        f.write('%s\n' % s)
    f.close()
def openFiletoArray(filename):
        f = open(filename)
        sortList = f.read().split()
        f.close()
        return sortList
def insertionSort(sortList):
    for e in range (1, len(sortList)):
        key = sortList[e]
        i = e - 1
        while i >= 0 and sortList[i] > key:
            sortList[i + 1] =  sortList[i]
            i = i - 1
        sortList[i + 1] = key
def mergeSort(sortList, l, r):
    if l < r:
        mid = (r + l) // 2
        mergeSort(sortList, l, mid)
        mergeSort(sortList,mid + 1, r)
        merge(sortList, l, mid, r)

def merge(sortList, l, mid, r):
    L = sortList[l:mid + 1]
    R = sortList[mid + 1:r + 1]
    L.append(str(math.inf))
    R.append(str(math.inf))
    i = 0
    j = 0
    k = 0
    for k in range(l, r + 1):
        if L[i] <= R[j]:
            sortList[k] = L[i]
            i = i + 1    
        else:
            sortList[k] = R[j]
            j = j + 1
def heapSort(sortList):
    buildMaxHeap(sortList)
    heapsize = len(sortList) - 1
    i = len(sortList) - 1
    while i >= 1:
        sortList[i],sortList[0] = sortList[0], sortList[i]
        i = i-1
        heapsize -= 1
        maxHeapify(sortList, heapsize, 0)
def buildMaxHeap(sortList):
    global bhstart
    global bhend
    bhstart = time.time()
    heapsize = len(sortList) - 1
    for i in range(len(sortList)//2, 0, -1):
        maxHeapify(sortList, heapsize, i)
    bhend = time.time()
def maxHeapify(sortList, heapsize, i):
    l = 2 * i + 1
    r = 2 * i + 2
    if l <= heapsize and sortList[l] > sortList[i]:
        largest = l
    else:
        largest = i
    if r <= heapsize and sortList[r] > sortList[largest]:
        largest = r
    if largest != i:
        sortList[i], sortList[largest] = sortList[largest], sortList[i]
        maxHeapify(sortList, heapsize, largest)

if __name__ == "__main__":
    filename = input("Enter the full name of the file you are trying to sort, ex. perm15K.txt ")
    ISList = openFiletoArray(filename)
    MSList = openFiletoArray(filename)
    HSList = openFiletoArray(filename)
    start = time.time()
    insertionSort(ISList)
    end = time.time()
    istime = end - start
    start = time.time()
    mergeSort(MSList, 0, len(MSList) - 1)
    end = time.time()
    mstime = end - start
    start = time.time()
    heapSort(HSList)
    end = time.time()
    hstime = end - start
    bhtime = bhend - bhstart
    insertionSorttoFile(ISList, filename)
    mergeSorttoFile(MSList, filename)
    heapSorttoFile(HSList, filename)
    print("Insertion Sort took ", istime, " seconds.")
    print("Merge Sort took ", mstime, " seconds.")
    print("Build Heap took ", bhtime, " seconds.")
    print("Heap Sort took ", hstime, " seconds.")
