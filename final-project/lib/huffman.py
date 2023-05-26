import heapq
from collections import defaultdict, Counter

class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def create_freq_table(data_list):
    return Counter(data_list)


def create_huffman_tree(freq_table):
    heap = [Node(char, freq) for char, freq in freq_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        
        merged = Node(None, node1.freq + node2.freq, node1, node2)
        heapq.heappush(heap, merged)

    return heap[0]  # The root node of the Huffman Tree


def create_code_table(root, code=''):
    if root is None:
        return {}

    if root.char is not None:
        return {root.char: code}

    code_table = {}
    code_table.update(create_code_table(root.left, code + '0'))
    code_table.update(create_code_table(root.right, code + '1'))
    
    return code_table


def huffman_encode(data_list):
    freq_table = create_freq_table(data_list)
    huffman_tree = create_huffman_tree(freq_table)
    code_table = create_code_table(huffman_tree)
    
    return code_table

def encode_data(data_list, code_table):
    return ''.join(code_table[char] for char in data_list)


# data = [1, 2, 'Z', 'E', 1]
# encoded_data = encode_data(data, code_table)
# table = huffman_encode(data)
# print(huffman_encode(data))
