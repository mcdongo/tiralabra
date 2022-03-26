from string import ascii_letters

class LZW:
    """Class which contains encoding and decoding methods
    for Lempel-Ziv-Welch algorithm
    """

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
        """
        keys = {}
        output_string = ''
        index = 0
        substring_pos = 1
        nth_value = 0
        
        while index + substring_pos <= len(input_string):
            substring = input_string[index:index+substring_pos]
            if substring in keys:
                substring_pos += 1
                continue
            keys[substring] = nth_value
            index += substring_pos
            substring_pos = 1
            nth_value += 1
            if len(substring) == 1:
                output_string += substring
            else:
                output_string += str(keys[substring[:-1]]) + substring[-1]
        
        if substring in keys:
            output_string += str(keys[substring])

        return output_string

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
        nth_value = 0

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

