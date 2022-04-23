import sys
import time
from lzw import LZW
from huffman import Huffman


def main():
    """Main function which checks given arguments and
    functions accordingly

    args:
        python3 src/main.py [compression method] [command] [filename]
    """
    if len(sys.argv) == 1:
        print("Please specify a command. Use -h for instructions.")
        return
    if sys.argv[1] == "-h":
        instructions()
        return
    if sys.argv[1] == "compare" and len(sys.argv) == 3:
        compare_algorithms()
        return
    if len(sys.argv) < 4:
        print("A file or compression method was not given. Use -h for instructions")
        return
    if sys.argv[2] == "compress":
        if sys.argv[1] == 'lzw':
            compress_lzw()
        if sys.argv[1] == 'huffman':
            compress_huffman()
    if sys.argv[2] == "decompress":
        if sys.argv[1] == 'lzw':
            decompress_lzw()
        if sys.argv[1] == 'huffman':
            decompress_huffman()
    if sys.argv[2] == "compare":
        if sys.argv[1] == "lzw":
            compare_lzw(sys.argv[3])
        if sys.argv[1] == "huffman":
            compare_huffman(sys.argv[3])


def instructions():
    """Function which prints instructions on how to use this app.
    """
    print("Command usage:")
    print("First argument presented must be the compression algorithm: either lzw or huffman.")
    print("Second argument presented must be either compress, decompress or compare.")
    print("Basic ascii characters are accepted. Present a file from normal_files directory.")
    print("Third argument presented must be the filename which the operation will be applied to.")
    print("Example: python3 main.py lzw compress test.txt\n")
    print("For decompression, the same applies however you have to present a file " +
          "from the packed_files directory.")
    print("Example: python3 main.py lzw decompress test.lzw\n")
    print("Comparison command compares the filesize between an " +
          "unpacked and packed instance of data.")
    print("Here again, second argument must be the algorithm desired and third the " +
          "filename of an unpacked .txt file.")
    print("Example: python3 main.py lzw compare test.txt\n")
    print("If you want to compare between lzw and huffman, give compare as the first argument " +
          "then an unpacked .txt file.")
    print("Example: python3 main.py compare sample.txt")


def compress_lzw():
    """Function which calls the lzw compression of a file."""
    compressed_string = lzw.handle_compression(sys.argv[3])
    print(f"Compressed string: {compressed_string}")


def decompress_lzw():
    """Function which calls the lzw decompression of a compressed file"""
    decompressed_string = lzw.handle_decompression(sys.argv[3])
    print(f"Decompressed string: {decompressed_string}")
    #print(f"Decompressed string: {lzw.decompress(sys.argv[2])}")


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


def compress_huffman():
    """Function which calls the Huffman coding compression of a file"""
    compressed_string = huff.handle_compression(sys.argv[3])
    print(f"Compressed string: {compressed_string}")


def decompress_huffman():
    """Function which calls the Huffman coding decompression of a file"""
    decompressed_string = huff.handle_decompression(sys.argv[3])
    print(f"Decompressed string: {decompressed_string}")


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


def compare_algorithms():
    """Function which compares the compression efficiency between
    LZW and Huffman coding"""
    lzw_size = compare_lzw(sys.argv[2])
    print()
    huff_size = compare_huffman(sys.argv[2])
    print()

    if not lzw_size or not huff_size:
        return

    if lzw_size < huff_size:
        print(f"LZW-compressed file is {round((huff_size - lzw_size)*100/huff_size, 2)}% smaller than " +
              "Huffman-compressed file.")
    else:
        print(f"Huffman-compressed file is {round((lzw_size - huff_size)*100/lzw_size, 2)}% smaller than " +
              "LZW-compressed file")


if __name__ == '__main__':
    start_time = time.time()
    lzw = LZW()
    huff = Huffman()
    main()
    end_time = time.time()
    print(f'It took {round(end_time-start_time, 3)}s to run the app')
