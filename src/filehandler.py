"""Module used to read and write files"""

import os
import json
from struct import pack, unpack

DIRNAME = os.path.dirname(__file__)
NORMAL_DIR = os.path.join(DIRNAME, 'normal_files')
PACKED_DIR = os.path.join(DIRNAME, 'packed_files')

if not os.path.isdir(PACKED_DIR):
    os.mkdir(PACKED_DIR)


def write_to_file(output, filename, path=NORMAL_DIR):
    """Write plain text to a file

    args:
        output: (str) String to be written
        filename: (str) Name of the file which the operation
            will be applied to (_decoded.txt) will be added
            to the end
        path: (str) Path to the directory in which the
            writing will take place (by default /normal_files)
    """
    filename = filename.split('.')
    with open(os.path.join(path, f"{filename[0]}_{filename[1]}_decoded.txt"), 'w') as file:
        file.write(output)


def write_to_coded_file(output, filename, path=PACKED_DIR):
    """Write LZW-compressed data to a file

    args:
        output: (List) List of bytes-like objects
        filename: (str) The name of the packed file
        path: (str) Path to the packed directory
    """
    filename = filename.split('.')[0]
    with open(os.path.join(path, f"{filename}.lzw"), 'wb') as file:
        for data in output:
            file.write((pack('>H', int(data))))


def read_from_input_file(input_file, path=NORMAL_DIR):
    """Reads plain text from a .txt file

    args:
        input_file: (str) The name of the file in question
        path: (str) Path to the wanted directory
    returns:
        input_string: (str) The contents of given file
    """
    with open(os.path.join(path, input_file), 'r') as file:
        input_string = file.read()

    return input_string


def read_from_coded_file(filename, path=PACKED_DIR):
    """Reads raw binary data compressed with lzw and unpacks it

    args:
        filename: (str) The name of the file in question
        path: (str) Path to the wanted directory
    returns:
        coded_array: (List) A list of integers
    """
    coded_array = []
    with open(os.path.join(path, filename), 'rb') as file:
        while True:
            byte = file.read(2)
            if len(byte) != 2:
                break
            (data, ) = unpack('>H', byte)
            coded_array.append(data)

    return coded_array


def get_size(filename, packed, normal_path=NORMAL_DIR, packed_path=PACKED_DIR):
    """Gets a size of a file in bytes

    args:
        filename: (str) The name of the file in question
        packed: (boolean) If true, packed_files directory, normal_files otherwise
        normal_path: (str) The path to the normal_files directory
        packed_path: (str) The path to the packed_files directory
    returns:
        size: (int) The size of a given file in bytes
        string: If the given file does not exist
    """
    try:
        if not packed:
            return os.path.getsize(os.path.join(normal_path, filename))
        return os.path.getsize(os.path.join(packed_path, filename))
    except FileNotFoundError:
        return "File not found"


def read_from_huffman_file(filename, path=PACKED_DIR):
    """Reads raw binary data from a .huf file

    args:
        filename (str): Name of the file in question
        path (str): Path of the wanted directory
    returns:
        data (str): A string consisting of integers
        dict: Contains huffman tree values
    """
    huffman_tree = ""
    with open(os.path.join(path, filename), 'rb') as file:
        while True:
            byte = file.read(1).decode()
            huffman_tree += byte
            if byte == '}':
                break

        data = file.read()

    return data, json.loads(huffman_tree)


def write_huffman_file(output, filename, huffman_tree, path=PACKED_DIR):
    """Writes data compressed with Huffman

    args:
        output (bytes): Raw binary data
        huffman_tree (dict): Huffman tree keys and values
        filename (str): Name of the file in question
        path (str): Path of the wanted directory
    """
    binary_huffman_tree = json.dumps(huffman_tree)
    with open(os.path.join(path, f"{filename.split('.')[0]}.huf"), 'wb') as file:
        file.write(binary_huffman_tree.encode())

    with open(os.path.join(path, f"{filename.split('.')[0]}.huf"), 'ab') as file:
        file.write(output)
