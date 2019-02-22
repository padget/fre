from unittest import TestCase, main
import fre.opregex as op


class OperatorFnRegexTest(TestCase):
    def test_foo(self):
        """

        """
        (op.a - op.z).match()


if __name__ == '__main__':
    main()
