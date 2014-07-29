# coding=utf-8
import unittest
from lib.models import Pedigree

__author__ = 'xeye'


class Case(unittest.TestCase):

    def test_inherited_probabilities(self):
        """inherited_probabilities calculates correctly"""
        mock = [['(']]
        pedigree = Pedigree(mock)
        self.assertEqual(pedigree.inherited((0, 1.0, 0), (0, 1.0, 0)),
                            (0.75*0.75, 0.75*0.25*2, 0.25*0.25)
                         )

if __name__ == '__main__':
    pass