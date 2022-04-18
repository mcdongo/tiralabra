# Testing

This repository has a CI which runs all tests on every push. The CI also checks if static code analysis with pylint scores a high enough score.

## LZW

Currently only basic unit tests are done. There are two sample text files in the tests/normal_files directory which are the files operated on. LZW's time complexity is O(n) since it goes through the input exactly once, its run time is very short even with large inputs. 100kB takes roughly 0.03 seconds and everything smaller takes less, on average. The algorithm is very efficient with files this large achieving up to 64% file size reduction.

![coverage](/documentation/coverage.png)