# Week report #2

This week I continued to study Lempel-Ziv-Welch compressing algorithm and actually managed to create a simple version of it. At the moment it only accepts strings with the English alphabet (no special symbols: commas, periods, etc. Not even spaces). The app is used at the moment through arguments given via terminal when launching the app, but this will later change. In the worst case the compressed message is actually larger than the original, but in others which have recurring patterns I managed to get even 50% compression rates. I did some basic unit tests to show that the conversion works in both directions and configured the repo with pylint and coverage. Next week I will continue to improve this algorithm, add the usage of different symbols and spaces and add the ability to have files to be compressed. The instructions to use this app can be launched with (from the root directory) with:

> python3 src/main.py -h

Tests can also be run with

> poetry run invoke test

Time spent this week: 10h