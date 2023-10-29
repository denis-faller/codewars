from collections import Counter, namedtuple
from heapq import heappush, heappop
def frequencies(strng):
    return list(Counter(strng).items())

def freqs2tree(freqs):
    heap, Node = [], namedtuple('Node', 'letter left right')
    for char, weight in freqs: heappush(heap, (weight, Node(char, None, None)))
    while len(heap) > 1:
        (w_left, left), (w_right, right) = heappop(heap), heappop(heap)
        heappush(heap, (w_left + w_right, Node("", left, right)))
    return heappop(heap)[1]

def encode(freqs, strng):
    def tree2bits(tree, parent_bits=1):
        if tree:
            if tree.letter: table[ord(tree.letter)] = bin(parent_bits)[3:]
            tree2bits(tree.left, parent_bits << 1 | 0)
            tree2bits(tree.right, parent_bits << 1 | 1)

    if len(freqs) > 1:
        table = {}
        tree2bits(freqs2tree(freqs))
        return strng.translate(table)

def decode(freqs, bits):
    def tree2strng(tree, parent_bits=1):
        if tree:
            if tree.letter: table[parent_bits] = tree.letter
            tree2strng(tree.left, parent_bits << 1 | 0)
            tree2strng(tree.right, parent_bits << 1 | 1)

    if len(freqs) > 1:
        table, code, strng = {}, 1, []
        tree2strng(freqs2tree(freqs))
        for b in map(int, bits):
            code = code << 1 | b
            if code in table:
                strng.append(table[code])
                code = 1
        return ''.join(strng)

s = 'aaaabcc'
print(frequencies(s))
print(encode(frequencies(s), s))
print(decode(frequencies(s), '1111000101'))