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


@dataclass(frozen=True)
class CharOperatorFnRegex:
    c: chr

    def __sub__(self, other: CharOperatorFnRegex) -> OperatorFnRegex:
        """Opérateur permettant de construire un
        CharInterval à partir de deux Char, le courant
        et l'other

        :param other: opérande de droite de l'opérateur
        :return: un nouveau CharInterval
        """

        return OperatorFnRegex(charinterval(self.c, other.c))

    def __call__(self, mt: MatchResult) -> MatchResult:
        """Execute le matching de la FnRegex wrappée

        :param mt: MatchResult servant de point de départ
                  pour le matching
        :return: le résultat de l'appel ```fnrx.match(m)```
        """

        return char(self.c)(mt)


def charop(__c: chr):
    """

    :param __c:
    :return:
    """
    return CharOperatorFnRegex(__c)


# lowers
a = charop('a')
b = charop('b')
c = charop('c')
d = charop('d')
e = charop('e')
f = charop('f')
g = charop('g')
h = charop('h')
i = charop('i')
j = charop('j')
k = charop('k')
l = charop('l')
m = charop('m')
n = charop('n')
o = charop('o')
p = charop('p')
q = charop('q')
r = charop('r')
s = charop('s')
t = charop('t')
u = charop('u')
v = charop('v')
w = charop('w')
x = charop('x')
y = charop('y')
z = charop('z')

# uppers
A = charop('A')
B = charop('B')
C = charop('C')
D = charop('D')
E = charop('E')
F = charop('F')
G = charop('G')
H = charop('H')
I = charop('I')
J = charop('J')
K = charop('K')
L = charop('L')
M = charop('M')
N = charop('N')
O = charop('O')
P = charop('P')
Q = charop('Q')
R = charop('R')
S = charop('S')
T = charop('T')
U = charop('U')
V = charop('V')
W = charop('W')
X = charop('X')
Y = charop('Y')
Z = charop('Z')

# digits
_0 = charop('0')
_1 = charop('1')
_2 = charop('2')
_3 = charop('3')
_4 = charop('4')
_5 = charop('5')
_6 = charop('6')
_7 = charop('7')
_8 = charop('8')
_9 = charop('9')

# intevals
lower = a - z
upper = A - Z
digit = _0 - _9

# ascii
__ = charop('_')
dquote = charop('"')
squote = charop('\'')
_and = charop('&')
