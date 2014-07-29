# coding=utf-8
from lib.utils import iterate_stream

__author__ = 'xeye'


# Any offspring of two heterozygous carriers
# has a 25% chance of inheriting a recessive disorder.
DOMINANT = 'A'
RECESSIVE = 'a'
MENDELIAN = 0.25


class ValidationError(StandardError):
    pass


class CalculationError(StandardError):
    pass


class Pedigree(object):
    """Pedigree tree handling"""

    def __init__(self, stream, dominant=DOMINANT, recessive=RECESSIVE):
        self.iterator = iterate_stream(stream)
        self.probabilities = {dominant + dominant: (1.0, 0, 0),
                              dominant + recessive: ((1.0 - MENDELIAN), 0, MENDELIAN),
                              recessive + recessive: (0, 0, 1.0)
                              }
        self.alleles = dominant, recessive

    def next(self):
        try:
            return self.iterator.next()
        except StopIteration:
            raise ValidationError("Iterator unexpectedly depleted")

    def swallow(self, required_char):
        """Simply pass required char"""
        if self.next() != required_char:
            raise ValidationError("Expected '%s', got %s" % (required_char, char))

    def inherited(self, triple1, triple2):
        """Probabilities to inherit alleles from given 2 parents

        Return probabilities in order (AA, Aa, aa)"""
        # Simple validation
        if not (sum(triple1) == sum(triple2) == 1.0):
            raise CalculationError("Triple %s or %s sum != 1.0" % (str(triple1), str(triple1)))

        dominant1 = triple1[0] + (1.0 - MENDELIAN) * triple1[1]
        recessive1 = triple1[2] + MENDELIAN * triple1[1]
        dominant2 = triple2[0] + (1.0 - MENDELIAN) * triple2[1]
        recessive2 = triple2[2] + MENDELIAN * triple2[1]

        return dominant1 * dominant2, \
               dominant1 * recessive2 + recessive1 * dominant2, \
               recessive1 * recessive2

    def triplet(self):
        """Recursive tree iteration

        Return probabilities in order (AA, Aa, aa)
        """
        char = self.next()
        if char == '(':
            t1 = self.triplet()
            self.swallow(',')
            t2 = self.triplet()
            self.swallow(')')
            return self.inherited(t1, t2)
        elif char in self.alleles:
            char2 = self.next()
            if char2 not in self.alleles:
                raise ValidationError("Expected '%s' or '%s" % self.alleles)
            return self.probabilities[char + char2]
        else:
            raise ValidationError("Unexpected symbol")

    def parse(self):
        """Parse pedigree in Newick format without cardinalities

        Return probabilities in order (AA, Aa, aa)
        """
        triplet = self.triplet()
        self.swallow(';')
        return triplet

