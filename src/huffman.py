from heapq import heappop, heappush
from filehandler import *


class PriorityQueue:
    """A class simplifying the use of a heap
    for the specific purpose to create a tree
    data structure for Huffman coding.
    """

    def __init__(self):
        self._elements = []
        self._priorities = {}

    def has_one_element(self):
        """Method which returns true if
        there is only one element in the _elements heap

        returns:
            boolean: True if only one element in heap
                False otherwise
        """
        return len(self._elements) == 1

    def insert(self, priority, info):
        """Method which inserts a tuple into
        the heap

        args:
            priority (int): The value which is used
                with sorting the heap
            info (Node): Node-object
        """
        if priority not in self._priorities:
            self._priorities[priority] = 0
        self._priorities[priority] += 1
        heappush(self._elements, (priority, self._priorities[priority], info))

    def get_nodes(self):
        """Method which returns all nodes
        in the same order from the heap."""
        return [x[2] for x in self._elements]

    def get_next(self):
        """Method which returns the next smallest
        value from the heap"""
        return heappop(self._elements)[2]


class Node:
    """Class used to create the necessary tree structure
    for Huffman coding"""

    def __init__(self, freq, symbol, left=None, right=None):
        """Class initializer

        args:
            freq (int): How many times this symbol
                appears in the source string
            symbol (str): A single character depicting this node
            left (Node): the left child of this node
            right (Node): the right child of this node
        """
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ''


class Huffman:
    """Class in charge of the Huffman coding compression
    and decompression algorithms.
    """

    def __init__(self):
        self.freq = {}
        self.codes = {}
        self.nodes = []

    def create_frequencies(self, text):
        """A method which goes through every single character
        in the source string and keeps track on how many times
        an individual character has been seen

        args:
            text (str): The source string
        returns:
            self.freq (dict): Keys are characters
                and values are occurences in the source string
        """
        self.freq = {}
        for character in text:
            if character not in self.freq:
                self.freq[character] = 0
            self.freq[character] += 1

        return self.freq

    def create_tree(self):
        """Method which creates a node for every unique character
        in the original source string forming a linked list

        returns:
            List: list of Node-objects
        """
        queue = PriorityQueue()

        for x in self.freq:
            queue.insert(self.freq[x], Node(self.freq[x], x))

        while not queue.has_one_element():
            left = queue.get_next()
            right = queue.get_next()

            left.huff = 0
            right.huff = 1

            new_node = Node(left.freq + right.freq, left.symbol +
                            right.symbol, left, right)

            queue.insert(left.freq + right.freq, new_node)

        self.nodes = queue.get_nodes()

    def merge_nodes(self, node, val=''):
        """Method which recursively starts to merge
        nodes into a tree structure

        args:
            node (Node): 
        """
        new_val = val + str(node.huff)

        if node.left:
            self.merge_nodes(node.left, new_val)
        if node.right:
            self.merge_nodes(node.right, new_val)

        if not node.left and not node.right:
            self.codes[node.symbol] = new_val

        return self.codes

    def compress(self, input_string):
        output_string = ""

        for character in input_string:
            output_string += str(self.codes[character])

        return output_string

    def handle_compression(self, filename, normal_dir=NORMAL_DIR, packed_dir=PACKED_DIR):
        try:
            text = read_from_input_file(filename, normal_dir)
        except FileNotFoundError:
            print("The specified file does ont exist.")
            return None

        self.create_frequencies(text)
        self.create_tree()
        self.codes = {}

        self.merge_nodes(self.nodes[0])
        compressed = self.compress(text)
        write_huffman_file(self.to_bytes(compressed), filename, packed_dir)
        write_json(filename, self.codes, packed_dir)

        return compressed

    def to_bytes(self, data):
        b = bytearray()
        for i in range(0, len(data), 8):
            b.append(int(data[i:i+8], 2))
        return bytes(b)

    def decompress(self, coded_string, codes):
        codes_reversed = {codes[x]: x for x in codes}
        substring = ''
        output_string = ''

        for bit in coded_string:
            substring += bit
            if substring in codes_reversed:
                output_string += codes_reversed[substring]
                substring = ''

        return output_string

    def handle_decompression(self, filename, normal_dir=NORMAL_DIR, packed_dir=PACKED_DIR):
        try:
            binary_string = read_from_huffman_file(filename, packed_dir)
            codes = read_json(filename)
        except FileNotFoundError:
            print("The specified file does not exist.")
            return None

        coded_string = ''
        for part in binary_string:
            coded_string += f"{part:08b}"

        decoded_text = self.decompress(coded_string, codes)
        write_to_file(decoded_text, filename, normal_dir)
        return decoded_text

    def handle_comparison(self, filename, normal_dir=NORMAL_DIR, packed_dir=PACKED_DIR):
        if not self.handle_compression(filename, normal_dir, packed_dir):
            return None
        unpacked_size = get_size(filename, False, normal_dir, packed_dir)
        filename = f"{filename.split('.')[0]}.huf"
        packed_size = get_size(filename, True, normal_dir, packed_dir)
        filename = f"{filename.split('.')[0]}.json"
        json_size = get_size(filename, True, normal_dir, packed_dir)
        print(unpacked_size, packed_size)
        return (unpacked_size, packed_size+json_size)
