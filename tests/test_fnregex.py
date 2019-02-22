from unittest import TestCase, main

from fre.fnregex import Repeat, Char, MatchResult, CharInterval, Sequence


def initial(inp: str) -> MatchResult:
    """Initialise un MatchResult avec l'inp (str)
    :param inp: string pour l'initialisation du MatchResult
    :return: un nouveau MatchResult
    """
    return MatchResult.input(inp)


class CharTest(TestCase):

    def test_char(self):
        char = Char('a')
        self.assertTrue(char.match(initial('aa')).matched(),
                        'on teste le cas ou est bon')
        self.assertFalse(char.match(initial('')).matched(),
                         'on teste le cas dune chaine vide')
        self.assertFalse(char.match(initial('b')).matched(),
                         'on teste le cas dune mauvaise correspondance')


class RepeatTest(TestCase):

    def test_repeat_char_case(self):
        """Teste si une simple répétition de Char
        est bien compris entre 1 et 4
        """

        repeat = Repeat(Char('a'), 1, 4)
        self.assertTrue(repeat.match(initial('aaa')).matched(),
                        'on teste le cas ou le nombre est dans l\'interval')
        self.assertFalse(repeat.match(initial('')).matched(),
                         'on teste le cas d\'une chaine vide')
        self.assertTrue(repeat.match(initial('abb')).matched(),
                        'on teste le cas d\'un nombre à la limite basse')
        self.assertTrue(repeat.match(initial('a')).matched(),
                        'on teste le cas d\'un nombre à la '
                        'limite basse sans suite')
        self.assertFalse(repeat.match(initial('bba')).matched(),
                         'on teste le cas on l\'on n\'est pas dans l\'interval')
        self.assertTrue(repeat.match(initial('aaaa')).matched(),
                        'on teste le cas on l\'on est sur le max')
        self.assertTrue(repeat.match(initial('aaaaa')).matched(),
                        'on teste le cas d\'un depassement d\'interval')

    def test_repeat_complex_case(self):
        """Teste si une simple répétition de CharInterval
        est bien compris entre 1 et 4
        """

        repeat = Repeat(CharInterval('a', 'z'), 1, 4)
        self.assertTrue(repeat.match(initial('abdj')).matched(),
                        'on teste le cas ou le nombre est dans l\'interval')
        self.assertFalse(repeat.match(initial('')).matched(),
                         'on teste le cas d\'une chaine vide')
        self.assertTrue(repeat.match(initial('a46546')).matched(),
                        'on teste le cas d\'un nombre à la limite basse')
        self.assertFalse(repeat.match(initial('46456a')).matched(),
                         'on teste le cas on l\'on n\'est pas dans l\'interval')
        self.assertTrue(repeat.match(initial('amzkldjal')).matched(),
                        'on teste le cas d\'un depassement d\'interval')


class SequenceTest(TestCase):

    def test_sequence_char_case(self):
        """Teste d'une sequence de deux char est suivi par
         différents cas
         """

        sequence = Sequence(Char('a'), Char('a'))
        self.assertTrue(sequence.match(initial('aa')).matched(),
                        'on teste le cas ou deux a se suivent bien')
        self.assertTrue(sequence.match(initial('aaa')).matched(),
                        'on teste le cas ou lon est au dela de la sequence')
        self.assertFalse(sequence.match(initial('a')).matched(),
                         'on teste le cas ou il manque un element')
        self.assertFalse(sequence.match(initial('')).matched(),
                         'on teste le cas ou linput est vide')

    def test_sequence_complex_case(self):
        """Teste dans un cas complexe si la sequence de deux
        elements complexe match bien avec les inputs
        """

        sequence = Sequence(Char('a'), Sequence(Char('b'), Char('c')))
        self.assertTrue(sequence.match(initial('abc')).matched(),
                        'on teste le cas passant nominal')
        self.assertTrue(sequence.match(initial('abcde')).matched(),
                        'on teste le cas passant avec du reste')
        self.assertFalse(sequence.match(initial('')).matched(),
                         'on teste le cas dun input vide')
        self.assertFalse(sequence.match(initial('ab')).matched(),
                         'on test le cas ko avec une chaine plus petite')
        self.assertFalse(sequence.match(initial('abeccsd')).matched(),
                         'on test le cas ko avec une chaine plus grande')


if __name__ == '__main__':
    main()
