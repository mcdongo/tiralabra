import unittest
import os
import shutil
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
            shutil.rmtree(PACKED_DIR)
            os.remove(os.path.join(NORMAL_DIR, 'sample1_decoded.txt'))
            os.remove(os.path.join(NORMAL_DIR, 'sample2_decoded.txt'))
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

    def test_3_sample1_decompression_and_input_file_content_equal(self):
        decoded_string = self.lzw.handle_decompression(
            'sample1.lzw', NORMAL_DIR, PACKED_DIR)

        content = read_from_input_file('sample1.txt', NORMAL_DIR)

        self.assertEqual(decoded_string, content)

    def test_4_sample2_decompression_and_input_file_content_equal(self):
        decoded_string = self.lzw.handle_decompression(
            'sample2.lzw', NORMAL_DIR, PACKED_DIR)

        content = read_from_input_file('sample2.txt', NORMAL_DIR)

        self.assertEqual(decoded_string, content)
