import argparse
import sys
import time
from lzw import LZW
from huffman import Huffman

PARSER = argparse.ArgumentParser(prog='main.py',
                                 description='Compression and decompression with LZW ' +
                                 'and Huffman coding algorithms')

PARSER.add_argument('Algorithm',
                    metavar='algorithm',
                    type=str,
                    help='lzw, huffman or both')

PARSER.add_argument('Operation',
                    metavar='operation',
                    type=str,
                    help='compress, decompress or compare')

PARSER.add_argument('Filename',
                    metavar='filename',
                    type=str,
                    help='name of the file, if compression is executed pass a ' +
                    'file from normal_files directory, ' +
                    'for decompression packed_files and ' +
                    'for comparison normal_files again.')


def main():
    """Main function which checks given arguments and
    functions accordingly

    args:
        python3 src/main.py [compression algorithm] [command] [filename]
    """
    if ARGS.Algorithm not in ('lzw', 'huffman', 'both'):
        print(f"{ARGS.Algorithm} is not a valid algorithm!")
        sys.exit(1)
    if ARGS.Operation not in ('compress', 'decompress', 'compare'):
        print(f"{ARGS.Operation} is not a valid operation!")
        sys.exit(1)

    if ARGS.Algorithm == 'lzw':
        if ARGS.Operation == 'compress':
            compress_lzw(ARGS.Filename)
        elif ARGS.Operation == 'decompress':
            decompress_lzw(ARGS.Filename)
        elif ARGS.Operation == 'compare':
            compare_lzw(ARGS.Filename)

    if ARGS.Algorithm == 'huffman':
        if ARGS.Operation == 'compress':
            compress_huffman(ARGS.Filename)
        elif ARGS.Operation == 'decompress':
            decompress_huffman(ARGS.Filename)
        elif ARGS.Operation == 'compare':
            compare_huffman(ARGS.Filename)

    if ARGS.Algorithm == 'both':
        if ARGS.Operation == 'compare':
            compare_algorithms(ARGS.Filename)
        elif ARGS.Operation == 'compress':
            compress_both(ARGS.Filename)
        elif ARGS.Operation == 'decompress':
            decompress_both(ARGS.Filename)


def compress_lzw(filename):
    """Function which calls the lzw compression of a file."""
    if lzw.handle_compression(filename):
        print("Done")


def decompress_lzw(filename):
    """Function which calls the lzw decompression of a compressed file"""
    if lzw.handle_decompression(filename):
        print("Done")


def compare_lzw(filename):
    """Function which compresses a given file and compares the
       filesize of the original with the compressed using lzw.
    """
    sizes = lzw.handle_comparison(filename)
    if sizes:
        print(f"Size of the unpacked file: {sizes[0]} bytes")
        print(f"Size of the packed file: {sizes[1]} bytes")
        print(
            "LZW-algorithm achieved a total of " +
            f"{round((sizes[0]-sizes[1])/sizes[0], 3)*100}% decrease in file size."
        )
        return sizes[1]
    return None


def compress_huffman(filename):
    """Function which calls the Huffman coding compression of a file"""
    if huff.handle_compression(filename):
        print("Done")


def decompress_huffman(filename):
    """Function which calls the Huffman coding decompression of a file"""
    if huff.handle_decompression(filename):
        print("Done")


def compare_huffman(filename):
    """Function which compares the file sizes between a Huffman-
    compressed file with a normal .txt file"""
    sizes = huff.handle_comparison(filename)
    if sizes:
        print(f"Size of the unpacked file: {sizes[0]} bytes")
        print(f"Size of the packed file: {sizes[1]} bytes")
        print(
            "Huffman coding algorithm achieved a total of " +
            f"{round((sizes[0]-sizes[1])/sizes[0],3)*100}% decrease in file size."
        )
        return sizes[1]
    return None


def compress_both(filename):
    """Function which calls for the compression of both algorithms"""
    if lzw.handle_compression(filename) and huff.handle_compression(filename):
        print('Done')


def decompress_both(filename):
    """Function which calls for the decompression of both algorithms"""
    filename = f"{filename.split('.')[0]}.lzw"
    lzw_res = lzw.handle_decompression(filename)
    filename = f"{filename.split('.')[0]}.huf"
    huf_res = huff.handle_decompression(filename)
    if lzw_res and huf_res:
        print("Done")


def compare_algorithms(filename):
    """Function which compares the compression efficiency between
    LZW and Huffman coding"""
    lzw_size = compare_lzw(filename)
    if not lzw_size:
        return
    print()
    huff_size = compare_huffman(filename)
    if not huff_size:
        return
    print()

    if lzw_size < huff_size:
        print(f"LZW-compressed file is {round((huff_size - lzw_size)*100/huff_size, 2)}% " +
              "smaller than Huffman-compressed file.")
    else:
        print(f"Huffman-compressed file is {round((lzw_size - huff_size)*100/lzw_size, 2)}% " +
              "smaller than LZW-compressed file")


if __name__ == '__main__':
    start_time = time.time()
    ARGS = PARSER.parse_args()
    lzw = LZW()
    huff = Huffman()
    main()
    end_time = time.time()
    print(f'It took {round(end_time-start_time, 3)}s to run the app')
