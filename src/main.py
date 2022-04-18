import sys
import time
from lzw import LZW


def main():
    """Main function which checks given arguments and
    functions accordingly

    args:
        python3 src/main.py [command] [filename]
    """
    if len(sys.argv) == 1:
        print("Please specify a command. Use -h for instructions.")
        return
    if sys.argv[1] == "-h":
        instructions()
        return
    if len(sys.argv) < 3:
        print("A file was not specified. Use -h for instructions")
        return
    if sys.argv[1] == "compress":
        compress()
    if sys.argv[1] == "decompress":
        decompress()
    if sys.argv[1] == "compare":
        compare()


def instructions():
    """Function which prints instructions on how to use this app.
    """
    print("Command usage:")
    print("First argument presented must be either compress, decompress or compare.")
    print("Basic ascii characters are accepted. Present a file from normal_files directory.")
    print("Second argument presented must be the filename which the operation will be applied to.")
    print("Example: python3 main.py compress test.txt\n")
    print("For decompression, the same applies however you have to present a file " +
          "from the packed_files directory.")
    print("Example: python3 main.py decompress test.lzw\n")
    print("Comparison command compares the filesize between an " +
          "unpacked and packed instance of data.")
    print("Here again, second argument must be the filename of an unpacked .txt file.")
    print("Example: python3 main.py compare test.txt")


def compress():
    """Function which calls the compression of a file."""
    compressed_string = lzw.handle_compression(sys.argv[2])
    print(f"Compressed string: {compressed_string}")


def decompress():
    """Function which calls the decompression of a compressed file"""
    decompressed_string = lzw.handle_decompression(sys.argv[2])
    print(f"Decompressed string: {decompressed_string}")
    #print(f"Decompressed string: {lzw.decompress(sys.argv[2])}")


def compare():
    """Function which compresses a given file and compares the
       filesize of the original with the compressed.
    """
    sizes = lzw.handle_comparison(sys.argv[2])
    if sizes:
        print(f"Size of the unpacked file: {sizes[0]} bytes")
        print(f"Size of the packed file: {sizes[1]} bytes")
        print(
            "LZW-algorithm achieved a total of " +
            f"{round((sizes[0]-sizes[1])/sizes[0], 3)*100}% decrease in file size.")


if __name__ == '__main__':
    start_time = time.time()
    lzw = LZW()
    main()
    end_time = time.time()
    print(f'It took {round(end_time-start_time, 3)}s to run the app')
