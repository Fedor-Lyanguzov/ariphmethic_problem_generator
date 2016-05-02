import unittest
from generator import *

class ProblemShould(unittest.TestCase):

    def test_multiply(self):
        p = Problem(2, "*", 3)
        self.assertEqual(6, p.c)

    def test_subtract(self):
        p = Problem(4, "-", 3)
        self.assertEqual(1, p.c)

    def test_add(self):
        p = Problem(2, "+", 3)
        self.assertEqual(5, p.c)

    def test_to_str(self):
        p = Problem(2, "+", 3)
        self.assertEqual("2 + 3 = 5", str(p))
    
    def test_format_output(self):
        p = Problem(1, "+", 2)
        res = p.format()
        self.assertEqual("1 + 2 = 3", res)

    def test_a_width(self):
        p1 = Problem(22, "*", 3)
        self.assertEqual(2, p1.a_width)

##class TaskShould(unittest.TestCase):
##
##    def test_to_str(self):
##        p1 = Problem(2, "*", 3)
##        p2 = Problem(2, "+", 3)
##        t = Task([p1, p2])
##        self.assertEqual("2 * 3 = 6\n2 + 3 = 5", str(t))
##
##    def test_deduce_format1(self):
##        p1 = Problem(22, "*", 3)
##        p2 = Problem(2, "+", 3)
##        t = Task([p1, p2])
##        self.assertEqual("{a:>2} {op} {b:<1} = {c:<2}", t.deduce_format())
##
##    def test_to_str_after_deducing_format(self):
##        p1 = Problem(22, "*", 3)
##        p2 = Problem(2, "+", 3)
##        t = Task([p1, p2])
##        self.assertEqual("22 * 3 = 66\n 2 + 3 = 5 ", str(t))


class FormattersShould(unittest.TestCase):

    def setUp(self):
        self.p1 = Problem(22, "*", 3)
        self.p2 = Problem(2, "+", 3)
        self.t = [self.p1, self.p2]
        
    def test_simple(self):
        self.assertEqual('\n'.join(map(str,self.t)), format_simple(self.t))
        
    def test_text_no_problems(self):
        self.assertEqual("No problems in task", format_text([]))

    def test_text(self):
        self.assertEqual("22 * 3 = 66\n 2 + 3 = 5 ", format_text(self.t))

class AdditionShould(unittest.TestCase):
    """
    1 + 2 = 3 - simple
    8 + 9 = 17 - simple over ten
    22 + 2 = 24 - complicated
    24 + 7 = 31 - complicated over ten
    43 + 22 = 65 - hard
    24 + 48 = 72 - hard over ten
    """

    def test_addition_eq(self):
        self.assertEqual(Problem(3, "+", 2), Addition(3, 2))

    def test_addition_ne(self):
        self.assertNotEqual(Problem(1, "+", 2), Addition(3, 2))

    def test_simple(self):
        task = [Addition.simple() for _ in range(100)]
        self.assertNotIn(False, [ 1 <= p.a <= 8 for p in task])
        self.assertNotIn(False, [ 1 <= p.b <= 8 for p in task])
        self.assertNotIn(False, [ p.c <= 9 for p in task])

    def test_simple_over_ten(self):
        task = [Addition.simple_over_ten() for _ in range(100)]
        errors = [ p for p in task if not 1 <= p.a <= 9 ]
        errors.extend([ p for p in task if not 1 <= p.b <= 9 ])
        errors.extend([ p for p in task if not 10 <= p.c <= 20 ])
        self.assertEqual([], errors)

    def test_complicated(self):
        task = [Addition.complicated() for _ in range(100)]
        errors = [ p for p in task if not 1 <= p.a <= 9 ]
        errors.extend([ p for p in task if not 1 <= p.b <= 9 ])
        errors.extend([ p for p in task if not 10 <= p.c <= 20 ])
        self.assertEqual([], errors)
        self.assertNotIn(False, [ 0 <= p.c%10 <= 9 for p in task])

    def test_complicated_over_ten(self):
        task = [Addition.complicated_over_ten() for _ in range(100)]
        res = [ p.a%10 + p.b%10 >= 10 for p in task ]
        #print([ (p.a, p.b) for p, r in zip(task, res) if not r])
        self.assertNotIn(False, res)
