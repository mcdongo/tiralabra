import unittest
from lzw import LZW

class TestLZW(unittest.TestCase):
    def setUp(self):
        self.lzw = LZW()

    def test_compression(self):
        to_compress = "ABBAACAABACAACABAAAC"
        compressed_string = self.lzw.compress(to_compress)[0]
        self.assertEqual(compressed_string, "AB257A256C256A258C260C256B260AC")

    def test_compression2(self):
        to_compress = "ABCABCCCBCCPAABCAWAIOHFAIOPSHAGWAMNSDASUAHDSUIAHWDAUIWDHAWUIOTIOEIOTAEHPTOAUIOPWEAOIJDSUIAHDYOGAWYTAWUIOTHAWUITHAWITASKJ"
        compressed_string = self.lzw.compress(to_compress)[0]
        self.assertEqual(compressed_string, "ABC256B258C258B260P256A257C256W256IOHF266OPS268AGW256MN272D256SU256HD272UI281W282A280I275D273W287OT284OE292T256E268P291O256U292P275E256O284J282S287A268DY267G265Y291A275U294H265U284T289I309SKJ")
    
    def test_decompression(self):
        to_decompress = "AB256B256C258B256A257B258A257C257A262C265BC262B263B267A257SF267F257F267BS273B256S278F279B277FI256U277KL277DJ288J256J289LW283IOP273H256O292I273J256PU273IA"
        original_string = "ABABACABBAABBABABCBABBCBABCBBBABABBABABSFBABFBFBABBSFBASFBFASBSFIAUSKLSDJJJAJJJLWIIOPFHAOWIFJAPUFIA"

        decompressed_string = self.lzw.decompress(to_decompress)
        self.assertEqual(original_string, decompressed_string)