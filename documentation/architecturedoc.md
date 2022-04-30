# Project execution

The project is used with a command line interface. The project has been split onto 4 different files, each with their own responsibilities. main.py module acts as the interface between the user and the algorithms. LZW and Huffman coding has been placed in their respective modules (lzw.py, huffman.py) and all classes, functions and methods of each algorithm can be found in these. Both of these use some functions and variables from filehandler.py module, which is in charge of everything related to files, like writing and reading them. 

## How they work & time complexity

### LZW

Time complexity for LZW is pretty straight-forward. LZW has to go through the input string exactly once. LZW generates keys on the go, meaning that it doesn't have to analyze the text in advance to create them. The algorithm forms a dict which has values from 0 to 255 as keys and their respective ascii character counterparts as values. Once the algorithm starts going through the string, every time it sees a new substring which is not yet in the dict, it adds it there. If that certain character or substring appears for the first time, it is vital to leave it as it is in the ouput string for later decompression. If this same substring appears again, its replaced with its key in the dictionary. The key value is incremented by one each time a new substring is added. After the compression is completed, the compressed contents is passed to the filehandler module which writes it into a .lzw binary data file. 

The big O notation for both compression and decompression for LZW is O(n). Decompression is basically the same as compression, but in a reverse order.

### Huffman coding

Huffman coding is more complicated. This algorithm has to go through the text beforehand to analyze the frequencies which characters appear in the text. After this, the algorithm has to create a Huffman tree with the use of a minimum heap. It goes through the dictionary containing every character and how many times it appeared in the source text and starts inserting them into the heap. After this, it starts to create the Huffman tree structure. The tree structure is formed with taking two nodes from the heap and combining their values (binary representation and combined frequency of the characters in these two nodes) to create a new node and adding it back to the heap. The general idea is that every time the tree is traversed to the left, you add a 0 to the representation of that symbol and right is the same except you add 1. Continue this, and when a node is found which have neither left or right children, you got the binary representation of that character. Every character has a unique representation this way, and no character has a representation which is a prefix of some other character's representation. The idea is that the most common symbols appear close to the top of the tree, requiring less bits in its binary representation and the ones which appear the least appear near the bottom, requiring the most bits. Now the algorithm goes recursively through the tree to create a dict containing all characters and their binary representations. Finally the algorithm replaces all characters with their binary representations and passes it forward with the dict containing the representations to the filehandler module. The codes are dumped as json string into the start of a .huf file and the rest of the content follows.

The total length of the compressed binary string before converting it into bytes is also added to the json-object. This is done because if the length of the compressed string is not divisible by 8, the algorithm can see where to stop reading when decompressing. This divisibility causes issues with compression as well: If for example the final character has a binary representation of 0111, the byte would be 0000 0111 instead of 0111 0000. With the total length this can be corrected before storing it into the file, as done in huffman.py to_bytes-method lines 172-176:

    coded_length = len(binary_array)*8
    offset_value = coded_length - len(data)
    if offset_value != 0:  # bitshift to correct the last byte
        # 0b00000111 -> 0b11100000
        binary_array[-1] = binary_array[-1] << offset_value

The offset value of how many bits it is from being divisible with 8 is taken and the final byte of the compressed array is bitshifted that many times to the left, correcting the byte. If this was not done, during decompression the final characters may be missing or be replaced with some other characters which should not be there.

Since the algorithm has to go through the input twice and take a minimum value from the heap a total of 2*(n-1) times (the heap is not static) having a complexity of O(log n). Inserting to the heap also takes O(log n). Thus the overall time complexity of Huffman coding is O(nlog n)