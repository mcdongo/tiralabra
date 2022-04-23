# Testing

This repository has a CI which runs all tests on every push. The CI also checks if static code analysis with pylint scores a high enough score.

## LZW

Currently only basic unit tests are done. There are two sample text files in the tests/normal_files directory which are the files operated on. LZW's time complexity is O(n) since it goes through the input exactly once, its run time is very short even with large inputs. 100kB takes roughly 0.03 seconds and everything smaller takes less, on average. The algorithm is very efficient with files this large achieving up to 64% file size reduction.

## Huffman coding

Unit tests are done with two pieces of sample data, one larger and one smaller. Since Huffman coding has to store the keys used in compression, its problems with small input files are more apparent. However with larger pieces of text, like the sample.txt in src/normal_files directory, Huffman still achieved a 46% decrease in file size, which is still remarkably good. There probably are a lot of ways to write the data more compactly than I have, resultin in smaller amount of wasted bits, but I am satisfied with my current approach. Huffman coding's time complexicty is O(nlogn) because of the tree structure it has to use. This can be seen in practice, however the time differences between LZW and Huffman coding are very insignificant from a human's point of view. With the same Lorem ipsum text, Huffman took about 0.08s which is a good result.

![coverage](/documentation/coverage.png)