import heapq
from typing import overload


class HuffTreeNode:
    def __init__(self, freq, index, left = None, right = None):
        self.freq = freq
        self.left = left
        self.right = right
        self.index = index
    
    def __gt__(self, other):
        return self.freq > other.freq
    
    def __lt__(self, other):
        return self.freq < other.freq
    

def traverse(node, arr, currCode):
    if node is None:
        return

    if node.left is None and node.right is None:
        if currCode == "":
            currCode = "0"
        arr.append((node.index, currCode))
        return

    traverse(node.left, arr, currCode + "0")
    traverse(node.right, arr, currCode + "1")



def createHuffmanTree(freqTable: list):
    #Create a node for every character, add to a minpq
    #We assign the two minimum frequencies, combine them and create a parent node to the two
    #Continue until we have only 2 left.
    #Find the root
    #Traverse the string again and translate each letter to corresponding code (Its own function)
    length = len(freqTable)

    minpq = []

    for i in range(length):
        tmp: HuffTreeNode = HuffTreeNode(freqTable[i], i)
        #Indexed by HuffTreeNode.freq
        heapq.heappush(minpq, tmp)

    while len(minpq) >= 2:
        firstOfTwo: HuffTreeNode = heapq.heappop(minpq)
        secondOfTwo: HuffTreeNode = heapq.heappop(minpq)


        parentNode: HuffTreeNode = HuffTreeNode(firstOfTwo.freq + secondOfTwo.freq, min(firstOfTwo.index, secondOfTwo.index), firstOfTwo, secondOfTwo)
        heapq.heappush(minpq, parentNode)
        #The following allows us to converge to 1 parent node at the end.. pop two, push one

    root = minpq[0]

    pairs = []
    traverse(root, pairs, "")

    codes = [''] * length
    for index, code in pairs:
        codes[index] = code
    return codes

def createHuffmanTreeDict(freqTable: dict):
    keys = list(freqTable.keys())
    length = len(keys)

    minpq = []

    for i in range(length):
        tmp: HuffTreeNode = HuffTreeNode(freqTable[keys[i]], i)
        heapq.heappush(minpq, tmp)

    while len(minpq) >= 2:
        firstOfTwo: HuffTreeNode = heapq.heappop(minpq)
        secondOfTwo: HuffTreeNode = heapq.heappop(minpq)

        parentNode: HuffTreeNode = HuffTreeNode(firstOfTwo.freq + secondOfTwo.freq, min(firstOfTwo.index, secondOfTwo.index), firstOfTwo, secondOfTwo)
        heapq.heappush(minpq, parentNode)

    root = minpq[0]

    pairs = []
    traverse(root, pairs, "")

    codes = {}
    for index, code in pairs:
        codes[keys[index]] = code
    return codes
