from filehandler import *


class LZW:
    """Class which contains encoding and decoding methods
    for Lempel-Ziv-Welch algorithm
    """

    def handle_compression(self, input_file, normal_dir=NORMAL_DIR, packed_dir=PACKED_DIR):
        """Method which reads the input string from a file
        and compresses it.
        Stores it into a desired file in packed_files folder.

        args:
            input_string (str): The filename the desired
                file
            normal_dir (str): The directory where unpacked
                files are located (by default /normal_files)
            packed_dir (str): The directory where packed
                files are located (by default /packed_files)
        returns:
            output_string (str): compressed version of the contents
                of input_string
            None if the input file specified does not exist
        """
        try:
            input_string = read_from_input_file(input_file, normal_dir)
        except FileNotFoundError:
            print('The file specified does not exist.')
            return None
        output_string, output_array = self.compress(input_string)
        write_to_coded_file(output_array, input_file, packed_dir)
        return output_string

    def handle_decompression(self, input_file, normal_dir=NORMAL_DIR, packed_dir=PACKED_DIR):
        """Method which reads compressed binary data from a specified
        file, runs it through the decompression algorithm and writes
        it into a normal text file.

        args:
            input_file (str): The filename in question
            normal_dir (str): The directory where normal
                files are located (by default /normal_files)
            packed_dir (str): The directory where compressed
                files are located (by default /packed files)
        returns:
            decoded_string (str): The contents of a compressed
                binary file converted into text
            None if the file specified can't be found
        """
        try:

            coded_array = read_from_coded_file(input_file, packed_dir)
        except FileNotFoundError:
            print('The specified file does not exist.')
            return None

        decoded_string = self.decompress(coded_array)
        write_to_file(decoded_string, input_file, normal_dir)

        return decoded_string

    def handle_comparison(self, input_file, normal_dir=NORMAL_DIR, packed_dir=PACKED_DIR):
        """Method which takes an input text file, compresses it
        and then compares the file size between the original with
        the compressed one.

        args:
            input_file (str): Name of the file in question
            normal_dir (str): The directory where normal
                files are located (by default /normal_files)
            packed_dir (str): The directory where compressed
                files are located (by default /packed_files)
        returns:
            unpacked_size (int), packed_size (int) (tuple):
                The sizes of said files
            None if the input file can't be found
        """
        if not self.handle_compression(input_file, normal_dir, packed_dir):
            return None
        unpacked_size = get_size(input_file, False, normal_dir, packed_dir)
        packed_size = get_size(input_file, True, normal_dir, packed_dir)

        return (unpacked_size, packed_size)

    def compress(self, input_string):
        """Method which applies the LZW-algorithm onto
        a string and returns a compressed version of it

        Args:
            input_string (str): string to be compressed
        Returns:
            output_string (str): compressed string
            output_array (list): a list containing all set integer
                values for certain strings and substrings
        """
        keys = {chr(x): x for x in range(256)}
        nth_value = 256
        output_string = ''
        output_array = []
        substring = ''

        for character in input_string:
            if substring + character in keys:
                substring += character
            else:
                output_string += str(keys[substring])
                output_array.append(keys[substring])
                keys[substring+character] = nth_value
                nth_value += 1
                substring = character

        output_string += str(keys[substring])
        output_array.append(keys[substring])

        return output_string, output_array

    def decompress(self, coded_array):
        """Method which decompresses a string which
        has been compressed with the LZW-algorithm.

        args:
            coded_array (list): a list containing
                integers which represent a character
                or a substring
        returns:
            output_string: decoded string
        """
        keys = {x: chr(x) for x in range(256)}
        output_string = ''
        nth_value = 256

        old_value = coded_array.pop(0)
        output_string += keys[old_value]
        for character in coded_array:
            if character not in keys:
                substring = keys[old_value] + last_character
            else:
                substring = keys[character]
            output_string += substring
            last_character = substring[0]
            keys[nth_value] = keys[old_value]+last_character
            nth_value += 1
            old_value = character

        print(f"decoded: {output_string}")
        return output_string
