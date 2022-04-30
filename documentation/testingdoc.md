# Testing

This repository has a CI which runs all tests on every push. The CI also checks if static code analysis with pylint scores a high enough score.
There are three sample text files in the tests/normal_files directory which are the files operated on. These three files consist of Wikipedia articles which have been cleared of not useful testing data (ie table of contents and links) in order to see how these algorithms handle "natural" language. Earlier I was using Lorem ipsum text, but it was pointed to me that samples like that are not really good for testing due to their somewhat recurring patterns.

The tests consist of taking a sample text file, compressing it and comparing the file sizes between the original file with the compressed file. Tests make sure that the compressed file is indeed smaller than the input. The second type of testing is to check if the compressed file actually has the same contents as original input file. Compressed files are run through the decompression algorithms and checked that they are indeed equal with the original pieces of text.

## LZW

LZW's time complexity is O(n) since it goes through the input exactly once, its run time is very short even with large inputs. 200kB takes roughly 0.07 seconds and everything smaller takes less, on average. The algorithm is very efficient with files this large achieving up to 55% file size reduction. Because the keys for compressing and decompressing with LZW are dynamically created in the text, meaning that they do not need to be separately stored, benefits this algorithm with smaller files, but when the length of the text grows larger, the keys start taking more and more bits reducing the compression efficiency. This can be somewhat nullified by keeping track of the amount of keys and resetting the code base at a certain number of keys. However, I have not implemented this.

## Huffman coding

Huffman coding has to store the keys used in compression, its problems with small input files are more apparent. The keys are stored in the beginning of each compressed file, thus resulting in a larger file size. However with larger pieces of text, like the sample2.txt in tests/normal_files directory, Huffman still achieved a 41.6% decrease in file size, which is still remarkably good. There probably are a lot of ways to write the data more compactly than I have, resulting in smaller amount of wasted bits, but I am satisfied with my current approach. Huffman coding's time complexity is O(nlogn) because of the tree structure it has to use. This can be seen in practice, however the time differences between LZW and Huffman coding are very insignificant from a human's point of view. With the same Wikipedia article, Huffman took about 0.08s which is a good result.


Tests can be run from the root directory with the command:

> poetry run invoke test

![coverage](/documentation/coverage.png)

## Wikipedia articles used
[Alan Turing](https://en.wikipedia.org/wiki/Alan_Turing)
[Lempel-Ziv-Welch](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch)
[Response to the COVID-19 pandemic in April 2020](https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_April_2020)