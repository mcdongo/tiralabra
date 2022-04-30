# Week 6

This week started with solving the issues I had by the end of last week. Now the Huffman tree is dumped into the beginning of the compressed file and the compression works well. Decompression also now works, as the output of decompression is equal to the contents of the input file. There were some problems with the final byte to be written, but I solved this with adding the total length of the compressed string into the dict, which contains the Huffman tree values. This value is used when decompressing, it tells when to stop while reading the last byte. This also required to fiddle with bitwise operations once again, because the way I had done the conversion to bytes formed the last byte wrong if the amount of bits was not divisible by 8. Now all of the unit tests work and the coverage these test reach is high. Thanks to the peer review i've got, I realized to quickly work on creating a more pleasing and easy-to-use interface, which I created with the argparse library. The use of program should be a lot easier now. The peer review also noted how much of my docstring was actually hindering the readability of the code. Before the final submission I have to clean up most of it and probably remove some unnecessary blocks of text. Unfortunately I had no time to create a gui this week, but it's not that important for this project. I created the project analysis document and instructions document now and updated the testing document. If I have time left, I will create a simple gui before the final submission.

Time spent this week: 12 hours