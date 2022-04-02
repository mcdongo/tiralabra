import sys
from lzw import LZW

def main():
    if len(sys.argv) == 1:
        print("Please specify a command. Use -h for instructions.")
        return
    if sys.argv[1] == "-h":
        instructions()
        return
    if len(sys.argv) < 3:
        print("A string was not given. Use -h for instructions")
        return
    if sys.argv[1] == "compress":
        compress()
    if sys.argv[1] == "decompress":
        decompress()
    if sys.argv[1] == "compare":
        compare()

def instructions():
    print("Command usage:")
    print("First argument presented must be either compress, decompress or compare.")
    print("Only basic characters in English alphabet are accepted.")
    print("Second argument presented must be the string which the operation will be applied to.")
    print("Example: python3 main.py compress ABBABBAGCTGCTBAAGTBCCTGAABCBCBCTGBABTAGBTCBB")

def compress():
    print(f"Compressed string: {lzw.handle_compression(sys.argv[2], 'testi.lzw')}")

def decompress():
    print(f"Decompressed string: {lzw.decompress(sys.argv[2])}")

def compare():
    to_encode = sys.argv[2] #'ABBABBAGCTGCTBAAGTBCCTGAABCBCBCTGBABTAGBTCBB'
    encoded = lzw.compress(to_encode)
    print(f"String to compress:\t{to_encode}")
    print(f"compressed string:\t{encoded}")
    print(f"original string length: {len(to_encode)}")
    print(f"compressed string length: {len(encoded)}")
    print(f"length of the compressed string is {round(len(encoded)/len(to_encode)*100, 2)}% of the length of the original string")

if __name__ == '__main__':
    lzw = LZW()
    main()
   