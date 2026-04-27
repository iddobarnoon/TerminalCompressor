import struct

from huffman import createHuffmanTree


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
        # Header: for each unique char, write its UTF-8 byte length, bytes, and frequency
        for char in unique_chars:
            char_bytes = char.encode('utf-8')
            f.write(struct.pack('>B', len(char_bytes)))
            f.write(char_bytes)
            f.write(struct.pack('>I', freq_map[char]))
        f.write(struct.pack('>I', total_bits))
        # Write the rest of the compressed file.       
        f.write(packed)


if __name__ == "__main__":
    encodeFile(r"C:\Users\iddob\Documents\CS Projects\TerminalCompressor\smallinput.txt")


