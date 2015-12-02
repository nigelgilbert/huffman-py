"""
Usage:
python3 huffman.py [encode.txt] [optional.txt]

Inputs:
encode.txt      : plain text file
optional.txt    : optional json text file name
"""
from sys import argv
from collections import defaultdict, deque
from heapq import heapify, heappop, heappush
import json


class Node:
    left = None
    right = None
    symbol = None
    val = 0

    def __init__(self, val, symbol):
        self.left = None
        self.right = None
        self.symbol = symbol
        self.val = val

    def __lt__(self, other):
        return self.val < other.val

    def __eq__(self, other):
        return self.val == other.val


_codes = {}
def encode(node, s=""):
    """
    Traverses the tree recursively, appending a binary digit for each edge.
    This makes a unique prefix-free binary code for each leaf node.
    Returns a dictionary of codes.
    """
    if node.symbol is not None:
        if not s:
            _codes[node.symbol] = "0"
        else:
            _codes[node.symbol] = s
    else:
        encode(node.left, s+"0")
        encode(node.right, s+"1")

    return _codes


def huffman(freqdict):
    """
    Generates a Huffman tree and returns the root Node.
    """
    heap = []
    for symbol in freqdict:
        heap.append(Node(freqdict[symbol], symbol));

    # Turns the list into a min heap.
    heapify(heap)

    # 1) Pop off 2 lowest values from min heap and make an internal node for them.
    # 2) Push the new parent node back onto heap.
    # 3) Continue until the heap is of size = 1, at which point the last value node
    #    in the heap is the root to our huffman tree.
    while len(heap) > 1:
        left = heappop(heap)
        right = heappop(heap)
        internal = Node(left.val + right.val, None)
        internal.left = left
        internal.right = right
        heappush(heap, internal) 

    return heap[0]


# Command line script starts here.
try:
    filename = argv[1]
    infile = open(filename)
except:
    print(__doc__)

freqdict = defaultdict(int)
unencoded = infile.read().lower()

for symbol in unencoded:
    freqdict[symbol] += 1

tree = huffman(freqdict)
codes = encode(tree)
encoded = "".join([codes[s] for s in unencoded])

if len(argv) is 3:
    outfile = open(argv[2], 'w+')
    outfile.write(json.dumps(codes))
    jsonencoded = '{"encoded": ' + json.dumps(encoded) + '}'
    outfile.write(jsonencoded)

for code in codes:
    print("symbol:", code, "frequency:", freqdict[code], "code:", codes[code])

print("\nString input:")
print(unencoded)
print("\nString input (binary ASCII):")
print("".join(format(ord(x), 'b') for x in unencoded))
print("\nEncoded output (binary Huffman code):")
print(encoded)

asciiratio = len(encoded) / float(len("".join(format(ord(x), 'b') for x in unencoded)))
print("\ncompression rate (ASCII): " + str(asciiratio))

ratioconst = len(encoded) /  float(5*len(unencoded))
print("compression rate (constant 5): " + str(ratioconst))