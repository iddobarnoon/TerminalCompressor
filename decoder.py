import struct
from huffman import HuffTreeNode, createHuffmanTreeDict, traverse


def decompressFile(path: str) -> None:
    with open(path, 'rb') as f:
        num_unique, = struct.unpack('>I', f.read(4))

        freq_map = {}
        for _ in range(num_unique):
            char_byte_len, = struct.unpack('>B', f.read(1))
            char = f.read(char_byte_len).decode('utf-8')
            freq, = struct.unpack('>I', f.read(4))
            freq_map[char] = freq

        total_bits, = struct.unpack('>I', f.read(4))
        packed = f.read()

        # print(freq_map)

    codes = createHuffmanTreeDict(freq_map)

    reverse_map = {code: char for char, code in codes.items()}
    bit_string = ''.join(f'{byte:08b}' for byte in packed)
    bit_string = bit_string[:total_bits]

    result = []
    current_code = ""
    for bit in bit_string:
        current_code += bit
        if current_code in reverse_map:
            result.append(reverse_map[current_code])
            current_code = ""
    decoded_text = ''.join(result)
    # out_path = path.replace('.txt', '_decoded.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(decoded_text)



if __name__ == "__main__":
    decompressFile(r"C:\Users\iddob\Documents\CS Projects\TerminalCompressor\smallinput.txt")