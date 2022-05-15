import unittest
import os
from lzw import LZW
from filehandler import *

DIRNAME = os.path.dirname(__file__)
NORMAL_DIR = os.path.join(DIRNAME, 'normal_files')
PACKED_DIR = os.path.join(DIRNAME, 'packed_files')


class TestLZW(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            os.mkdir(PACKED_DIR)
        except Exception:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(os.path.join(PACKED_DIR, 'sample1.lzw'))
            os.remove(os.path.join(PACKED_DIR, 'sample2.lzw'))
            os.remove(os.path.join(PACKED_DIR, 'sample3.lzw'))
            os.remove(os.path.join(NORMAL_DIR, 'sample1_lzw_decoded.txt'))
            os.remove(os.path.join(NORMAL_DIR, 'sample2_lzw_decoded.txt'))
            os.remove(os.path.join(NORMAL_DIR, 'sample3_lzw_decoded.txt'))
        except Exception:
            pass

    def setUp(self):
        self.lzw = LZW()

    def test_1_sample1_packed_smaller_than_original(self):
        sizes = self.lzw.handle_comparison(
            'sample1.txt', NORMAL_DIR, PACKED_DIR)

        self.assertLess(sizes[1], sizes[0])

    def test_2_sample2_packed_smaller_than_original(self):
        sizes = self.lzw.handle_comparison(
            'sample2.txt', NORMAL_DIR, PACKED_DIR)

        self.assertLess(sizes[1], sizes[0])

    def test_3_sample3_packed_smaller_than_original(self):
        sizes = self.lzw.handle_comparison(
            'sample3.txt', NORMAL_DIR, PACKED_DIR)

        self.assertLess(sizes[1], sizes[0])

    def test_4_sample1_decompression_and_input_file_content_equal(self):
        decoded_string = self.lzw.handle_decompression(
            'sample1.lzw', NORMAL_DIR, PACKED_DIR)

        content = read_from_input_file('sample1.txt', NORMAL_DIR)

        self.assertEqual(decoded_string, content)

    def test_5_sample2_decompression_and_input_file_content_equal(self):
        decoded_string = self.lzw.handle_decompression(
            'sample2.lzw', NORMAL_DIR, PACKED_DIR)

        content = read_from_input_file('sample2.txt', NORMAL_DIR)

        self.assertEqual(decoded_string, content)

    def test_6_sample_3_decompression_and_input_file_content_equal(self):
        decoded_string = self.lzw.handle_decompression(
            'sample3.lzw', NORMAL_DIR, PACKED_DIR)

        content = read_from_input_file('sample3.txt', NORMAL_DIR)

        self.assertEqual(decoded_string, content)
