import sys, os
from string import ascii_letters

DIRNAME = os.path.dirname(__file__)
INPUT_DIR = os.path.join(DIRNAME, 'input_files')
OUTPUT_DIR = os.path.join(DIRNAME, 'output_files')

class LZW:
    """Class which contains encoding and decoding methods
    for Lempel-Ziv-Welch algorithm
    """

    def handle_compression(self, input_string, output_filename):
        if len(input_string) > 3:
            if input_string[-4::] == ".txt":
                with open(os.path.join(INPUT_DIR, input_string), "r") as file:
                    input_string = file.read()
        output_string, output_array = self.compress(input_string)
        self.write_to_file(output_array, output_filename)
        return output_string

    def compress(self, input_string):
        """Method which accepts a single string as an argument
        (At the moment only basic ascii letters are accepted)
        and compresses it by using a dictionary approach.
        Patterns which are seen multiple times inside a given
        string will be replaced with a key.

        Args:
            input_string (str): string to be compressed
        Returns:
            output_string (str): compressed string
            output_array (list): an array of 2-byte long bytes objects
        Raises:
            ValueError if input_string contains a character which is not
                in the first 256 values of ascii mapping
        """
        keys = {}
        output_string = ''
        output_array = []
        index = 0
        substring_pos = 1
        nth_value = 256
        
        while index + substring_pos <= len(input_string):
            substring = input_string[index:index+substring_pos]

            if ord(substring[-1]) > 255:
                raise ValueError
            if substring in keys:
                substring_pos += 1
                continue

            keys[substring] = nth_value
            index += substring_pos
            substring_pos = 1
            nth_value += 1

            if len(substring) == 1:
                output_string += substring
                output_array.append(ord(substring).to_bytes(2, sys.byteorder))
            else:
                output_string += str(keys[substring[:-1]]) + substring[-1]
                output_array.append(int(keys[substring[:-1]]).to_bytes(2, sys.byteorder))
                output_array.append(ord(substring[-1]).to_bytes(2, sys.byteorder))
        
        """if substring in keys:
            output_string += str(keys[substring])"""

        return output_string, output_array

    def write_to_file(self, output_array, filename):
        with open(os.path.join(OUTPUT_DIR, filename), "wb") as file:
            for byte in output_array:
                file.write(byte)

    def decompress(self, coded_string):
        """A method which accepts a single already encoded string
        and decodes it in a reverse order compared to the encode method.

        Args:
            coded_string (str): compressed string
        Returns:
            output_string: decoded string
        """
        keys = {}
        output_string = ''
        index = 0
        substring_pos = 1
        nth_value = 256

        while index + substring_pos <= len(coded_string):
            substring = coded_string[index:index+substring_pos]
            if len(substring) == 1 and substring in ascii_letters:
                keys[str(nth_value)] = substring
                nth_value += 1
                index += substring_pos
                substring_pos = 1
                output_string += substring
                continue
            if substring[-1] in ascii_letters:
                combined = keys[substring[:-1]] + substring[-1]
                keys[str(nth_value)] = combined
                output_string += combined
                nth_value += 1
                index += substring_pos
                substring_pos = 1
                continue
            substring_pos += 1

        if substring in keys and output_string[:-substring_pos-1] != keys[substring]:
            output_string += keys[substring]

        print(f"decoded: {output_string}")
        return(output_string)

