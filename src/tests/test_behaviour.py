# coding=utf-8
import os
import unittest
from lib.models import ValidationError, Pedigree

__author__ = 'xeye'


class TestBehaviour(unittest.TestCase):

    def test_data_load(self):
        """Data loaded correctly"""
        filename = os.path.join(os.path.dirname(__file__), 'fixtures', 'data.txt')
        with open(filename) as infile:
            pedigree = Pedigree(infile)
            self.assertEqual(pedigree.parse(), (0.6037673950195312, 0.3474884033203125, 0.04874420166015625))


    def test_syntax(self):
        """Bad data raises exception"""
        filename = os.path.join(os.path.dirname(__file__), 'fixtures', 'bad_data.txt')
        with open(filename) as infile:
            pedigree = Pedigree(infile)
            self.assertRaises(ValidationError, pedigree.parse)

if __name__ == '__main__':
    pass