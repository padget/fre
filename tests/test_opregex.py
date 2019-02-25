from unittest import TestCase, main

import fre.opregex as op
from fre.fnregex import MatchResult


class OperatorFnRegexTest(TestCase):
    def test_foo(self):
        """

        """
        (op.a - op.z)(MatchResult.input('a'))


if __name__ == '__main__':
    main()
