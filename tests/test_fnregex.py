from unittest import TestCase, main

from fre.fnregex import Repeat, Char, MatchResult, CharInterval, Sequence


def initial(inp: str) -> MatchResult:
    return MatchResult.input(inp)


class CharTest(TestCase):

    def test_char(self):
        char = Char('a')
        self.assertTrue(char.match(MatchResult.input('aa')).matched(),
                        'on teste le cas ou est bon')
        self.assertFalse(char.match(MatchResult.input('')).matched(),
                         'on teste le cas dune chaine vide')
        self.assertFalse(char.match(MatchResult.input('b')).matched(),
                         'on teste le cas dune mauvaise correspondance')


class RepeatTest(TestCase):

    def test_repeat_char_case(self):
        """Teste si une simple répétition de Char
        est bien compris entre 1 et 4
        """

        repeat = Repeat(Char('a'), 1, 4)
        self.assertTrue(repeat.match(MatchResult.input('aaa')).matched(),
                        'on teste le cas ou le nombre est dans l\'interval')
        self.assertFalse(repeat.match(MatchResult.input('')).matched(),
                         'on teste le cas d\'une chaine vide')
        self.assertTrue(repeat.match(MatchResult.input('abb')).matched(),
                        'on teste le cas d\'un nombre à la limite basse')
        self.assertTrue(repeat.match(MatchResult.input('a')).matched(),
                        'on teste le cas d\'un nombre à la '
                        'limite basse sans suite')
        self.assertFalse(repeat.match(MatchResult.input('bba')).matched(),
                         'on teste le cas on l\'on n\'est pas dans l\'interval')
        self.assertTrue(repeat.match(MatchResult.input('aaaa')).matched(),
                        'on teste le cas on l\'on est sur le max')
        self.assertTrue(repeat.match(MatchResult.input('aaaaa')).matched(),
                        'on teste le cas d\'un depassement d\'interval')

    def test_repeat_complex_case(self):
        """Teste si une simple répétition de CharInterval
        est bien compris entre 1 et 4
        """

        repeat = Repeat(CharInterval('a', 'z'), 1, 4)
        self.assertTrue(repeat.match(MatchResult.input('abdj')).matched(),
                        'on teste le cas ou le nombre est dans l\'interval')
        self.assertFalse(repeat.match(MatchResult.input('')).matched(),
                         'on teste le cas d\'une chaine vide')
        self.assertTrue(repeat.match(MatchResult.input('a46546')).matched(),
                        'on teste le cas d\'un nombre à la limite basse')
        self.assertFalse(repeat.match(MatchResult.input('46456a')).matched(),
                         'on teste le cas on l\'on n\'est pas dans l\'interval')
        self.assertTrue(repeat.match(MatchResult.input('amzkldjal')).matched(),
                        'on teste le cas d\'un depassement d\'interval')


class SequenceTest(TestCase):
    def test_sequence_test_char_case(self):
        sequence = Sequence(Char('a'), Char('a'))
        self.assertTrue(sequence.match(initial('aa')),
                        'on teste le cas ou deux a se suivent bien')


if __name__ == '__main__':
    main()
