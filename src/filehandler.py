import os
from struct import pack, unpack

DIRNAME = os.path.dirname(__file__)
NORMAL_DIR = os.path.join(DIRNAME, 'normal_files')
PACKED_DIR = os.path.join(DIRNAME, 'packed_files')


def write_to_file(output, filename, path=NORMAL_DIR):
    """Function which writes a plain string into a file

    args:
        output: (str) String to be written
        filename: (str) Name of the file which the operation
            will be applied to (_decoded.txt) will be added
            to the end
        path: (str) Path to the directory in which the
            writing will take place (by default /normal_files)
    """
    filename = filename.split('.')[0]
    with open(os.path.join(path, f"{filename}_decoded.txt"), 'w') as file:
        file.write(output)


def write_to_coded_file(output, filename, path=PACKED_DIR):
    """Function which writes compressed binary data into a file

    args:
        output: (List) List of bytes-like objects packed with
            the struct-library
        filename: (str) The name of the file which the operation
            will be applied to (file format will be discarded
            and changed to .lzw)
        path: (str) Path to the directory in which the
            writing will take place (by default /packed_files)
    """
    filename = filename.split('.')[0]
    with open(os.path.join(path, f"{filename}.lzw"), 'wb') as file:
        for data in output:
            file.write((pack('>H', int(data))))


def read_from_input_file(input_file, path=NORMAL_DIR):
    """Function which reads the contents of a given plain
        text file

    args:
        input_file: (str) The name of the file in question
        path: (str) Path to the directory in which the
            reading will take place (by default /normal_files)
    returns:
        input_string: (str) The contents of given file
    """
    with open(os.path.join(path, input_file), 'r') as file:
        input_string = file.read()

    return input_string


def read_from_coded_file(filename, path=PACKED_DIR):
    """Function which reads the contents of a compressed binary
        file and unpacks it with the struct-library

    args:
        filename: (str) The name of the file in question
        path: (str) Path to the directory in which the
            reading will take place (by default /packed_files)
    returns:
        coded_array: (List) A list of integers which all depict
            a character or a substring
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
    """Function which returns the size of a given file in bytes

    args:
        filename: (str) The name of the file in question
        packed: (boolean) depicts whether or not to use
            normal files or packed files
        normal_path: (str) The path to the directory containing
            normal text files (by default /normal_files)
        packed_path: (str) The path to the directory containing
            compressed binary files (by default packed_files)
    returns:
        size: (int) The size of a given file in bytes
        string: If the given file does not exist
    """
    try:
        if not packed:
            return os.path.getsize(os.path.join(normal_path, filename))
        return os.path.getsize(os.path.join(packed_path, f"{filename.split('.')[0]}.lzw"))
    except FileNotFoundError:
        return "File not found"
