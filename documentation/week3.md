# Week 3

This week I added the ability to use all of the basic ascii characters which are contained in a single byte (values 0-255). Also the possibility to output the compressed file into a file. At the moment the data is being written with each character taking 2 bytes of space, which doesn't make the compression side very efficient. Next week I'm planning to modify this so that every character only takes 11-12bits of space in order to actually make the compression shrink the file size. The app now also accepts input files. In order to use them, just create a .txt file inside the input_files folder and pass the name of that file when calling compression from the terminal. This will output the "compressed" contents into said file. A single string can still be passed for the app without ending the argument with .txt. At the moment these "compressed" files can't be read, but that's something for next week.

> python3 src/main.py compress textfile.txt

Time spent this week: 12 hours