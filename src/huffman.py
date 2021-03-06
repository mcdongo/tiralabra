from heapq import heappop, heappush
import filehandler as fh


class PriorityQueue:
    """A class simplifying the use of a heap
    for the specific purpose to create a tree
    data structure for Huffman coding.
    """

    def __init__(self):
        self._elements = []
        self._priorities = {}

    def has_one_element(self):
        """Returns true if the heap only has one element"""
        return len(self._elements) == 1

    def insert(self, priority, info):
        """Inserts a tuple into the heap

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
        """Creates a dict which keeps track how many times
        an unique symbol has appeared in the source text

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
        """Creates the Huffman tree data structure"""
        queue = PriorityQueue()

        for key, value in self.freq.items():
            queue.insert(value, Node(value, key))

        while not queue.has_one_element():
            left = queue.get_next()
            right = queue.get_next()

            left.huff = 0
            right.huff = 1

            new_node = Node(left.freq + right.freq, left.symbol +
                            right.symbol, left, right)

            queue.insert(left.freq + right.freq, new_node)

        self.nodes = queue.get_nodes()

    def form_codes(self, node, val=''):
        """Goes through the Huffman tree recursively and saves
        the binary reprsentation for each symbol into a dict

        Args:
            node (Node): current Node in question
            val (str): The binary reprsentation of a node in the Huffman tree
        Returns:
            self.codes (dict): Huffman tree keys and values
        """

        new_val = val + str(node.huff)

        if node.left:
            self.form_codes(node.left, new_val)
        if node.right:
            self.form_codes(node.right, new_val)

        if not node.left and not node.right:
            self.codes[node.symbol] = new_val

        return self.codes

    def compress(self, input_string):
        """Compresses a given string with
        the codes from the Huffman tree

        Args:
            input_string (str): Text to be compressed
        Returns:
            output_string (str): String converted to Huffman tree values
        """
        output_string = ""

        for character in input_string:
            output_string += str(self.codes[character])
        return output_string

    def handle_compression(self, filename, normal_dir=fh.NORMAL_DIR, packed_dir=fh.PACKED_DIR):
        """Handles everything related to compressing a file

        Args:
            filename (str): Name of the source file
            normal_dir (str): Directory in which the source file is located
            packed_dir (str): Directory where compressed files are saved
        Returns:
            compressed (str): Text converted to Huffman tree values
        """
        try:
            text = fh.read_from_input_file(filename, normal_dir)
        except FileNotFoundError:
            print("The specified file does not exist.")
            return None

        self.create_frequencies(text)
        self.create_tree()
        self.codes = {}

        self.form_codes(self.nodes[0])
        compressed = self.compress(text)
        self.codes['length'] = len(compressed)
        fh.write_huffman_file(self.to_bytes(compressed),
                              filename, self.codes, packed_dir)

        return compressed

    def to_bytes(self, data):
        """Takes a converted string and converts it further
        to bytes.

        Args:
            data (str): converted text
        Returns:
            binary_array (Bytes): converted data to be written
        """
        binary_array = bytearray()
        for i in range(0, len(data), 8):
            # if amount of bits is not divisible by 8, writes last byte "in reverse"
            binary_array.append(int(data[i:i+8], 2))

        coded_length = len(binary_array)*8
        offset_value = coded_length - len(data)
        if offset_value != 0:  # bitshift to correct the last byte
            # 0b00000111 -> 0b11100000
            binary_array[-1] = binary_array[-1] << offset_value

        return bytes(binary_array)

    def decompress(self, coded_string, codes):
        """Decompresses data with Huffman tree values

        Args:
            coded_string (str): binary written continuously
            codes (dict): Huffman tree keys and values
        Returns:
            output_string (str): Decompressed string
        """
        codes_reversed = {codes[x]: x for x in codes}
        substring = ''
        output_string = ''

        for bit in coded_string:
            substring += bit
            if substring in codes_reversed:
                output_string += codes_reversed[substring]
                substring = ''

        return output_string

    def handle_decompression(self, filename, normal_dir=fh.NORMAL_DIR, packed_dir=fh.PACKED_DIR):
        """Handles everything related to decompressing a file

        Args:
            filename (str): Name of the source file
            normal_dir (str): Directory in which the source file is located
            packed_dir (str): Directory where compressed files are saved
        Returns:
            decoded_text (str): Decompressed text
        """
        try:
            binary_string, codes = fh.read_from_huffman_file(
                filename, packed_dir)
        except FileNotFoundError:
            print("The specified file does not exist.")
            return None

        coded_string = ''
        for part in binary_string:
            coded_string += f"{part:08b}"

        length_diff = len(coded_string) - codes['length']
        if length_diff != 0:
            # OUTPUT SHOULD BE SAME AS ORIGINAL INPUT NOW
            coded_string = coded_string[:-length_diff+1]

        decoded_text = self.decompress(coded_string, codes)
        fh.write_to_file(decoded_text, filename, normal_dir)
        return decoded_text

    def handle_comparison(self, filename, normal_dir=fh.NORMAL_DIR, packed_dir=fh.PACKED_DIR):
        """Compares the file size between a compressed instace of data with
        the source file

        Args:
            filename (str): Name of the source file
            normal_dir (str): Directory in which the source file is located
            packed_dir (str): Directory where compressed files are saved
        Returns:
            (unpacked_size (int), packed_size(int)): file sizes in bytes
        """
        if not self.handle_compression(filename, normal_dir, packed_dir):
            return None
        unpacked_size = fh.get_size(filename, False, normal_dir, packed_dir)
        filename = f"{filename.split('.')[0]}.huf"
        packed_size = fh.get_size(filename, True, normal_dir, packed_dir)

        return (unpacked_size, packed_size)
