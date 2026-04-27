import heapq
import struct
from typing import Counter


"""
Given a path, we encode whatever text is in there
"""
def encode(string) -> str:
    #What I need to do
    #1. extract into string or array
    #2. construct frequency table
    #3. construct huffman tree
    #4. Pre-Order-Traversal each part of array to get encode
    uniqueChars = []
    freqTable = []

    for character in string:
        if character in uniqueChars:
            freqTable[uniqueChars.index(character)] += 1
        else:
            uniqueChars.append(character)
            freqTable.append(1)

    codes = createHuffmanTree(freqTable)

    codeMap = {}
    for index, character in enumerate(uniqueChars):
        codeMap[character] = codes[index]

    encodedString = ""

    for char in string:
        encodedString += codeMap[char]

    print(encodedString)
    return encodedString
    

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



def createHuffmanTree(freqTable):
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


def encodeFile(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content:
        return

    freq_map = {}
    for char in content:
        freq_map[char] = freq_map.get(char, 0) + 1

    unique_chars = list(freq_map.keys())
    freq_table = [freq_map[c] for c in unique_chars]

    codes = createHuffmanTree(freq_table)
    code_map = {char: codes[i] for i, char in enumerate(unique_chars)}

    bit_string = ''.join(code_map[char] for char in content)
    total_bits = len(bit_string)

    padding = (8 - total_bits % 8) % 8
    bit_string += '0' * padding

    packed = bytearray()
    for i in range(0, len(bit_string), 8):
        packed.append(int(bit_string[i:i+8], 2))

    with open(path, 'wb') as f:
        f.write(struct.pack('>I', len(unique_chars)))
        for char in unique_chars:
            char_bytes = char.encode('utf-8')
            f.write(struct.pack('>B', len(char_bytes)))
            f.write(char_bytes)
            f.write(struct.pack('>I', freq_map[char]))
        f.write(struct.pack('>I', total_bits))
        f.write(packed)


if __name__ == "__main__":
    encodeFile(r"C:\Users\iddob\Documents\CS Projects\TerminalCompressor\test.txt")


