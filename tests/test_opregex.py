from unittest import TestCase, main

import fre.opregex as op
from fre.fnregex import MatchResult


def initial(inp: str) -> MatchResult:
    """Initialise un MatchResult avec l'inp (str)
    :param inp: string pour l'initialisation du MatchResult
    :return: un nouveau MatchResult
    """
    return MatchResult.input(inp)


class OperatorFnRegexTest(TestCase):
    def test_interval(self):
        """Teste si un interval est bien
        construit et matche bien avec l'input
        fourni au test
        """

        self.assertTrue((op.a - op.z)(initial('a')).matched())
        self.assertTrue((op.a - op.z)(initial('c')).matched())
        self.assertTrue((op.a - op.z)(initial('z')).matched())
        self.assertFalse((op.a - op.z)(initial('')).matched())
        self.assertFalse((op.a - op.z)(initial('!aaaa')).matched())

    def test_sequence(self):
        """Teste si une sequence est bien
        construite et matche bien avec l'input
        fourni au test
        """

        az = op.a >> op.z
        self.assertTrue(az(initial('az')).matched())
        self.assertTrue(az(initial('azss')).matched())
        self.assertFalse(az(initial('')).matched())
        self.assertFalse(az(initial('!aaaa')).matched())
        a_z = op.a - op.z
        aza_z = az >> a_z
        self.assertTrue(aza_z(initial('azaa')).matched())
        self.assertFalse(aza_z(initial('az!a')).matched())

    def test_choice(self):
        """Teste si une sequence est bien
        construite et matche bien avec l'input
        fourni au test
        """

        a__z = op.a | op.z
        self.assertTrue(a__z(initial('a')).matched())
        self.assertTrue(a__z(initial('z')).matched())
        self.assertFalse(a__z(initial('b')).matched())
        self.assertFalse(a__z(initial('')).matched())
        a_z = op.a - op.z
        a__za_z = a__z >> a_z
        self.assertTrue(a__za_z(initial('ab')).matched())
        self.assertTrue(a__za_z(initial('za')).matched())
        self.assertFalse(a__za_z(initial('bc')).matched())
        self.assertFalse(a__za_z(initial('')).matched())

    def test_repeat(self):
        """Teste si une sequence est bien
        construite et matche bien avec l'input
        fourni au test
        """

        aaaaa = op.a[:5]
        self.assertTrue(aaaaa(initial('aaaaa')).matched())
        self.assertTrue(aaaaa(initial('aaaaaaaa')).matched())
        self.assertTrue(aaaaa(initial('b')).matched())
        self.assertTrue(aaaaa(initial('')).matched())
        _aaaaa = op.a[1:5]
        self.assertTrue(_aaaaa(initial('aaaaa')).matched())
        self.assertTrue(_aaaaa(initial('aaaaaaaa')).matched())
        self.assertFalse(_aaaaa(initial('b')).matched())
        self.assertFalse(_aaaaa(initial('')).matched())
        a_z = op.a - op.z
        aaaaaa_z = aaaaa >> a_z
        self.assertTrue(aaaaaa_z(initial('aaaaab')).matched())
        self.assertTrue(aaaaaa_z(initial('aaaaaza')).matched())
        self.assertFalse(aaaaaa_z(initial('aaaaa!c')).matched())
        self.assertFalse(aaaaaa_z(initial('')).matched())

    def test_email(self):
        """Teste si une regex d'email match bien"""
        name = op.lower[1:10]
        email = name >> op.dot >> name >> op.at >> name >> op.dot >> name
        self.assertTrue(email(initial('padget.pro@gmail.com')).matched())
        self.assertFalse(email(initial('padget.pro!gmail.com')).matched())
        email_cpx = name >> ((op.dot >> name)[0:1]) >> op.at >> name >> op.dot >> name
        self.assertTrue(email_cpx(initial('padget@gmail.com')).matched())
        self.assertFalse(email_cpx(initial('padget!gmail.com')).matched())


if __name__ == '__main__':
    main()
