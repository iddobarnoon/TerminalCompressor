# Terminal File Compressor

A file compression and decompression tool built on Huffman coding, with a simple GUI.

I learned about Huffman coding in my Design and Analysis of Algorithms class and wanted to build this little tool for myself — decided to share it on GitHub in case anyone else finds it useful.

## How it works

Huffman coding is a lossless compression algorithm that assigns shorter bit sequences to more frequent characters and longer sequences to rarer ones. The result is a binary encoding of the file that takes up less space than the original.

**Compression steps:**
1. Read the file and build a character frequency table
2. Construct a min-heap priority queue from the frequencies
3. Repeatedly pop the two lowest-frequency nodes, merge them into a parent, and push it back — until one root node remains
4. Traverse the tree to assign a unique binary code to each character
5. Re-encode the file using those codes and write the compressed binary, along with a header storing the frequency table needed for decompression

**Decompression** reads the header to reconstruct the same Huffman tree, then decodes the bit stream back to the original text.

## Features

- Lossless compression and decompression of text files
- GUI built with [Dear PyGui](https://github.com/hoffstadt/DearPyGui)
- Shows file size before and after (KB) with compression ratio

## Usage

```bash
pip install -r requirements.txt
python interface.py
```

1. Click **Browse** to select a text file
2. Click **Compress** to compress it in-place
3. Click **Decompress** to restore the original text

> **Note:** The file is modified in-place. Keep a copy of the original if you need it.

## Project structure

```
huffman.py      # Huffman tree construction and traversal
encoder.py      # Reads a text file and writes compressed binary
decoder.py      # Reads compressed binary and restores original text
interface.py    # Dear PyGui GUI
```
