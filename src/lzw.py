import filehandler as fh


class LZW:
    """Class which contains encoding and decoding methods
    for Lempel-Ziv-Welch algorithm
    """

    def handle_compression(self, input_file, normal_dir=fh.NORMAL_DIR, packed_dir=fh.PACKED_DIR):
        """Handles everything necessary to compress a file

        args:
            input_file (str): Desired source file
            normal_dir (str): Directory of the source file
            packed_dir (str): Desired export directory
        returns:
            output_string (str): compressed version of the source file
            None if the input file specified does not exist
        """
        try:
            input_string = fh.read_from_input_file(input_file, normal_dir)
        except FileNotFoundError:
            print('The specified file does not exist.')
            return None
        output_string, output_array = self.compress(input_string)
        fh.write_to_coded_file(output_array, input_file, packed_dir)
        return output_string

    def handle_decompression(self, input_file, normal_dir=fh.NORMAL_DIR, packed_dir=fh.PACKED_DIR):
        """Handles everything necessary to decompress a file

        args:
            input_file (str): Desired source file
            normal_dir (str): Directory of the source file
            packed_dir (str): Desired export directory
        returns:
            decoded_string (str): decompressed version of the source file
            None if the input file specified does not exist
        """
        try:

            coded_array = fh.read_from_coded_file(input_file, packed_dir)
        except FileNotFoundError:
            print('The specified file does not exist.')
            return None

        decoded_string = self.decompress(coded_array)
        fh.write_to_file(decoded_string, input_file, normal_dir)

        return decoded_string

    def handle_comparison(self, input_file, normal_dir=fh.NORMAL_DIR, packed_dir=fh.PACKED_DIR):
        """Compares the file size between a compressed instace of data with
        the source file

        Args:
            input_file (str): Name of the source file
            normal_dir (str): Directory in which the source file is located
            packed_dir (str): Directory where compressed files are saved
        Returns:
            (unpacked_size (int), packed_size(int)): file sizes in bytes
        """
        if not self.handle_compression(input_file, normal_dir, packed_dir):
            return None
        unpacked_size = fh.get_size(input_file, False, normal_dir, packed_dir)
        input_file = f"{input_file.split('.')[0]}.lzw"
        packed_size = fh.get_size(input_file, True, normal_dir, packed_dir)

        return (unpacked_size, packed_size)

    def compress(self, input_string):
        """Compresses a string with the LZW algorithm

        Args:
            input_string (str): string to be compressed
        Returns:
            output_string (str): compressed string
            output_array (list): every element in list is a single character
                coded with lzw
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
        """Decompresses a string with LZW decompression
        algorithm

        args:
            coded_array (list): a list containing
                integers which represent a character
                or a substring
        returns:
            output_string (str): decoded string
        """
        keys = {x: chr(x) for x in range(256)}
        last_character = coded_array[0]
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
            keys[nth_value] = keys[old_value] + last_character
            nth_value += 1
            old_value = character

        return output_string
