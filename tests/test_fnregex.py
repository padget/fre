from unittest import TestCase, main

from fre.fnregex import repeat, char, MatchResult, charinterval, seq, choice


def initial(inp: str) -> MatchResult:
    """Initialise un MatchResult avec l'inp (str)
    :param inp: string pour l'initialisation du MatchResult
    :return: un nouveau MatchResult
    """
    return MatchResult.input(inp)


class CharTest(TestCase):

    def test_char(self):
        ch = char('a')
        self.assertTrue(ch(initial('aa')).matched(),
                        'on teste le cas ou est bon')
        self.assertFalse(ch(initial('')).matched(),
                         'on teste le cas dune chaine vide')
        self.assertFalse(ch(initial('b')).matched(),
                         'on teste le cas dune mauvaise correspondance')


class RepeatTest(TestCase):

    def test_repeat_char_case(self):
        """Teste si une simple répétition de Char
        est bien compris entre 1 et 4
        """

        rep = repeat(char('a'), 1, 4)
        self.assertTrue(rep(initial('aaa')).matched(),
                        'on teste le cas ou le nombre est dans l\'interval')
        self.assertFalse(rep(initial('')).matched(),
                         'on teste le cas d\'une chaine vide')
        self.assertTrue(rep(initial('abb')).matched(),
                        'on teste le cas d\'un nombre à la limite basse')
        self.assertTrue(rep(initial('a')).matched(),
                        'on teste le cas d\'un nombre à la '
                        'limite basse sans suite')
        self.assertFalse(rep(initial('bba')).matched(),
                         'on teste le cas on l\'on n\'est pas dans l\'interval')
        self.assertTrue(rep(initial('aaaa')).matched(),
                        'on teste le cas on l\'on est sur le max')
        self.assertTrue(rep(initial('aaaaa')).matched(),
                        'on teste le cas d\'un depassement d\'interval')

    def test_repeat_complex_case(self):
        """Teste si une simple répétition de CharInterval
        est bien compris entre 1 et 4
        """

        rep = repeat(charinterval('a', 'z'), 1, 4)
        self.assertTrue(rep(initial('abdj')).matched(),
                        'on teste le cas ou le nombre est dans l\'interval')
        self.assertFalse(rep(initial('')).matched(),
                         'on teste le cas d\'une chaine vide')
        self.assertTrue(rep(initial('a46546')).matched(),
                        'on teste le cas d\'un nombre à la limite basse')
        self.assertFalse(rep(initial('46456a')).matched(),
                         'on teste le cas on l\'on n\'est pas dans l\'interval')
        self.assertTrue(rep(initial('amzkldjal')).matched(),
                        'on teste le cas d\'un depassement d\'interval')


class SequenceTest(TestCase):

    def test_sequence_char_case(self):
        """Teste d'une sequence de deux char est suivi par
         différents cas
         """

        sequence = seq(char('a'), char('a'))
        self.assertTrue(sequence(initial('aa')).matched(),
                        'on teste le cas ou deux a se suivent bien')
        self.assertTrue(sequence(initial('aaa')).matched(),
                        'on teste le cas ou lon est au dela de la sequence')
        self.assertFalse(sequence(initial('a')).matched(),
                         'on teste le cas ou il manque un element')
        self.assertFalse(sequence(initial('')).matched(),
                         'on teste le cas ou linput est vide')

    def test_sequence_complex_case(self):
        """Teste dans un cas complexe si la sequence de deux
        elements complexe match bien avec les inputs
        """

        sequence = seq(char('a'), char('b'), char('c'))
        self.assertTrue(sequence(initial('abc')).matched(),
                        'on teste le cas passant nominal')
        self.assertTrue(sequence(initial('abcde')).matched(),
                        'on teste le cas passant avec du reste')
        self.assertFalse(sequence(initial('')).matched(),
                         'on teste le cas dun input vide')
        self.assertFalse(sequence(initial('ab')).matched(),
                         'on test le cas ko avec une chaine plus petite')
        self.assertFalse(sequence(initial('abeccsd')).matched(),
                         'on test le cas ko avec une chaine plus grande')


class ChoiceTest(TestCase):

    def test_choice_char_case(self):
        cho = choice(char('c'), char('a'))
        self.assertTrue(cho(initial('a')).matched())
        self.assertFalse(cho(initial('b')).matched())
        self.assertFalse(cho(initial('')).matched())

    def test_choice_char_interval_case(self):
        cho = choice(charinterval('0', '8'), char('e'))
        self.assertTrue(cho(initial('4')).matched())
        self.assertFalse(cho(initial('b')).matched())
        self.assertFalse(cho(initial('')).matched())

    def test_choice_three_case(self):
        cho = choice(charinterval('0', '8'), char('e'), char('c'))
        self.assertTrue(cho(initial('c')).matched())
        self.assertFalse(cho(initial('b')).matched())
        self.assertFalse(cho(initial('')).matched())


if __name__ == '__main__':
    main()
