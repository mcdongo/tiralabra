import unittest
from lzw import LZW

class TestLZW(unittest.TestCase):
    def setUp(self):
        self.lzw = LZW()

    def test_compression(self):
        to_compress = "ABBAACAABACAACABAAAC"
        compressed_string = self.lzw.compress(to_compress)
        self.assertEqual(compressed_string, "AB1A0C0A2C4C0B4AC9")

    def test_compression2(self):
        to_compress = "ABCABCCCBCCPAABCAWAIOHFAIOPSHAGWAMNSDASUAHDSUIAHWDAUIWDHAWUIOTIOEIOTAEHPTOAUIOPWEAOIJDSUIAHDYOGAWYTAWUIOTHAWUITHAWITASKJ"
        compressed_string = self.lzw.compress(to_compress)
        self.assertEqual(compressed_string, "ABC0B2C2B4P0A1C0W0IOHF10OPS12AGW0MN16D0SU0HD16UI25W26A24I19D17W31OT28OE36T0E12P35O0U36P19E0O28J26S31A12DY11G9Y35A19U38H9U28T33I53SKJ61")
    
    def test_decompression(self):
        to_decompress = "AB0B0C2B0A1B2A1C1A6C9BC6B7B11A1SF11F1F11BS17B0S22F23B21FI0U21KL21DJ32J0J33LW27IOP17H0O36I17J0PU17I0"
        original_string = "ABABACABBAABBABABCBABBCBABCBBBABABBABABSFBABFBFBABBSFBASFBFASBSFIAUSKLSDJJJAJJJLWIIOPFHAOWIFJAPUFIA"

        decompressed_string = self.lzw.decompress(to_decompress)
        self.assertEqual(original_string, decompressed_string)