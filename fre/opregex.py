"""Le module opregex permet la mise en place d'opérateur
sur les FnRegex. Ce qui permet de ne pas utiliser
directement les constructeurs des FnRegex mais plutot
les opérateurs à la sauce regex et donc d'offrir une
lecture plus agréable des expressions régulière ainsi
créés.

De plus, le module met à disposition un ensemble de FnRegex
construite de base afin de pouvoir les composer dans des
constructions plus complexes d'expressions régulières
"""

from __future__ import annotations

import string
from dataclasses import dataclass

from fre.fnregex import FnRegex, repeat, choice, charinterval, MatchResult, \
    seq, char


@dataclass(frozen=True)
class OperatorFnRegex(FnRegex):
    """Un OperatorFnRegex permet de wrapper un
    FnRegex afin de lui fournir une surchage des
    opérateur permettant de construire des FnRegex
    non pas à partir des constructeurs (fastidieux)
    mais plutôt à partir des opérateurs exposés

    TODO mettre des exemples d'opérateurs

    """

    fnrx: FnRegex

    def __call__(self, mt: MatchResult) -> MatchResult:
        """Execute le matching de la FnRegex wrappée

        :param mt: MatchResult servant de point de départ
                  pour le matching
        :return: le résultat de l'appel ```fnrx.match(m)```
        """

        return self.fnrx(mt)

    def __sub__(self, other: OperatorFnRegex) -> OperatorFnRegex:
        """Opérateur permettant de construire un
        CharInterval à partir de deux Char, le courant
        et l'other

        :param other: opérande de droite de l'opérateur
        :return: un nouveau CharInterval
        """

        return OperatorFnRegex(charinterval(self.fnrx.char, other.fnrx.char))

    def __or__(self, other: OperatorFnRegex) -> OperatorFnRegex:
        """Construit un FnRegex de type Choice

        :param other: l'autre choix
        :return: un nouveau Choice
        """

        return OperatorFnRegex(choice(self.fnrx, other.fnrx))

    def __getitem__(self, sl: slice):
        """Construit un FnRegex de type Repeat

        :param sl: les limites min et max du Repeat
        :return: un nouveau Repeat
        """

        if isinstance(sl, slice):
            start = sl.start
            stop = sl.stop
            return OperatorFnRegex(repeat(self.fnrx, start, stop))
        else:
            raise AttributeError('Only slice with two integers '
                                 'is implemented : \n'
                                 ' - rex[1:5],\n'
                                 ' - rex[:12],\n'
                                 ' - rex[12:]')

    def __rshift__(self, other: OperatorFnRegex) -> OperatorFnRegex:
        """Construit un FnRegex de type Sequence

        :param other: suite de la séquence
        :return: une nouvelle Sequence
        """

        return OperatorFnRegex(seq(self.fnrx, other.fnrx))


def op(fnrx: FnRegex) -> OperatorFnRegex:
    """Construit un OperatorFnRegex à partir
    d'un FnRegex

    :param fnrx: à wrapper dans un OperatorFnRegex
    :return: un nouveau OperatorFnRegex
    """

    return OperatorFnRegex(fnrx)


# lowers
a = op(char('a'))
b = op(char('b'))
c = op(char('c'))
d = op(char('d'))
e = op(char('e'))
f = op(char('f'))
g = op(char('g'))
h = op(char('h'))
i = op(char('i'))
j = op(char('j'))
k = op(char('k'))
l = op(char('l'))
m = op(char('m'))
n = op(char('n'))
o = op(char('o'))
p = op(char('p'))
q = op(char('q'))
r = op(char('r'))
s = op(char('s'))
t = op(char('t'))
u = op(char('u'))
v = op(char('v'))
w = op(char('w'))
x = op(char('x'))
y = op(char('y'))
z = op(char('z'))

# uppers
A = op(char('A'))
B = op(char('B'))
C = op(char('C'))
D = op(char('D'))
E = op(char('E'))
F = op(char('F'))
G = op(char('G'))
H = op(char('H'))
I = op(char('I'))
J = op(char('J'))
K = op(char('K'))
L = op(char('L'))
M = op(char('M'))
N = op(char('N'))
O = op(char('O'))
P = op(char('P'))
Q = op(char('Q'))
R = op(char('R'))
S = op(char('S'))
T = op(char('T'))
U = op(char('U'))
V = op(char('V'))
W = op(char('W'))
X = op(char('X'))
Y = op(char('Y'))
Z = op(char('Z'))

# digits
_0 = op(char('0'))
_1 = op(char('1'))
_2 = op(char('2'))
_3 = op(char('3'))
_4 = op(char('4'))
_5 = op(char('5'))
_6 = op(char('6'))
_7 = op(char('7'))
_8 = op(char('8'))
_9 = op(char('9'))

# intevals
lower = a - z
upper = A - Z
digit = _0 - _9

# ascii
__ = op(char('_'))
dquote = op(char('"'))
squote = op(char('\''))
_and = op(char('&'))

