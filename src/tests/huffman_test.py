import unittest
import os
from huffman import Huffman
from filehandler import *

DIRNAME = os.path.dirname(__file__)
NORMAL_DIR = os.path.join(DIRNAME, 'normal_files')
PACKED_DIR = os.path.join(DIRNAME, 'packed_files')


class TestHuffman(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            os.mkdir(PACKED_DIR)
        except Exception:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(os.path.join(PACKED_DIR, 'sample1.huf'))
            os.remove(os.path.join(PACKED_DIR, 'sample2.huf'))
            os.remove(os.path.join(PACKED_DIR, 'sample1.json'))
            os.remove(os.path.join(PACKED_DIR, 'sample2.json'))
            os.remove(os.path.join(NORMAL_DIR, 'sample1_huf_decoded.txt'))
            os.remove(os.path.join(NORMAL_DIR, 'sample2_huf_decoded.txt'))
        except Exception:
            pass

    def setUp(self):
        self.huffman = Huffman()

    def test_1_sample1_packed_smaller_than_original(self):
        sizes = self.huffman.handle_comparison(
            'sample1.txt', NORMAL_DIR, PACKED_DIR)

        self.assertLess(sizes[1], sizes[0])

    def test_2_sample2_packed_smaller_than_original(self):
        sizes = self.huffman.handle_comparison(
            'sample2.txt', NORMAL_DIR, PACKED_DIR)

        self.assertLess(sizes[1], sizes[0])

    """def test_3_sample1_decompression_and_input_file_content_equal(self):
        decoded_string = self.huffman.handle_decompression(
            'sample1.huf', NORMAL_DIR, PACKED_DIR)

        content = read_from_input_file('sample1.txt', NORMAL_DIR)

        self.assertEqual(decoded_string, content)

    def test_4_sample2_decompression_and_input_file_content_equal(self):
        decoded_string = self.huffman.handle_decompression(
            'sample2.huf', NORMAL_DIR, PACKED_DIR)

        content = read_from_input_file('sample2.txt', NORMAL_DIR)

        self.assertEqual(decoded_string, content)"""
