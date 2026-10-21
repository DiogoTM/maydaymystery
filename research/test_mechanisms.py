import unittest

import sympy as S

from mechanism_tests import structure


class ExactAlgebraTests(unittest.TestCase):
    def test_known_sl2_brackets(self):
        e = S.Matrix([[0, 1], [0, 0]])
        f = e.T
        h = S.diag(1, -1)
        outside, adj = structure([e, f, h])
        self.assertEqual(outside, [])
        self.assertEqual(adj[0][:, 1], S.Matrix([0, 0, 1]))
        self.assertEqual(adj[2][:, 0], S.Matrix([2, 0, 0]))
        self.assertEqual(adj[2][:, 1], S.Matrix([0, -2, 0]))

    def test_nonclosed_span_is_rejected(self):
        e = S.Matrix([[0, 1], [0, 0]])
        outside, _ = structure([e, e.T])
        self.assertEqual(outside, [[0, 1], [1, 0]])


if __name__ == '__main__':
    unittest.main()
