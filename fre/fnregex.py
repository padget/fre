from dataclasses import dataclass
from sys import maxsize


@dataclass(frozen=True)
class MatchResult:
    """MatchResult représente un résultat de la fonction match
    implémentée par les FnRegex
    """

    value: str
    index: int = 0
    match: bool = True

    def at_end(self) -> bool:
        """Retourne True si le parcourt de la value est
        arrivé à son terme.

        :return: Si l'index de parcourt est supérieur ou
                 égale à la longueur de la value alors
                 True sinon False
        """

        return self.index >= len(self.value)

    def not_end(self) -> bool:
        """Fonction exactement equivalente à
        ```not at_ent()```

        :return:
        """

        return not self.at_end()

    def char(self):
        """Permet d'obtenir le caractère
        courrant à lire

        :return: le caractère courant
        """

        return self.value[self.index]

    def matched(self) -> bool:
        """Donne le résultat du dernier test de
        correspondance ayant été fait sur le caractère courant

        :return: True si cela a matché, False sinon
        """

        return self.match

    def ok(self):
        """Construit un MatchResult ayant
        avancé de 1 son index et avec un résultat
        de matching à True

        :return: un nouveau MatchResult
        """

        return MatchResult(self.value, self.index + 1, True)

    def current_ok(self):
        """Construit un MatchResult ayant un résultat
        de matching à True mais restant sur son index
        de parcourt actuel

        :return: un nouveau MatchResult
        """

        return MatchResult(self.value, self.index, True)

    def bad(self):
        """Construit un MatchResult ayant un résultat
        de matching à False et restant donc sur son
        index de parcourt actuel

        :return: Un nouveau MatchResult
        """

        return MatchResult(self.value, self.index, False)

    @staticmethod
    def input(value: str):
        """Construit un MatchResult dans son état
        initial avec un index de parcourt à 0 et
        son match à True

        :return: un nouveau MatchResult
        """

        return MatchResult(value)


@dataclass(frozen=True)
class FullMatchResult:

    mr: MatchResult

    def matched(self) -> bool:
        """Si le dernier test de matching est True et
        que l'index de parcourt est au terme dans la
        valeur, alors on retourne True, False sinon

        :return: True si à la fin et que cela matche,
                False sinon
        """
        return self.mr.at_end() and self.mr.matched()


class FnRegex:
    def __init__(self):
        pass

    def match(self, m: MatchResult) -> MatchResult:
        pass

    def __or__(self, other):
        return Choice(self, other)

    def __getitem__(self, sl: slice):
        if isinstance(sl, slice):
            start = sl.start
            stop = sl.stop
            return Repeat(self, start, stop)
        else:
            raise AttributeError('Only slice with two integers '
                                 'is implemented : \n'
                                 ' - rex[1:5],\n'
                                 ' - rex[:12],\n'
                                 ' - rex[12:]')

    def __rshift__(self, other):
        return Sequence(self, other)


class Sequence(FnRegex):
    def __init__(self,
                 left: FnRegex,
                 right: FnRegex):
        super().__init__()
        self.left = left
        self.right = right

    def match(self, m: MatchResult) -> MatchResult:
        lresult = self.left.match(m)

        if lresult.matched():
            rresult = self.right.match(lresult)

            if rresult.matched():
                return rresult

        return m


class Repeat(FnRegex):
    def __init__(self,
                 re: FnRegex,
                 start: int,
                 stop: int,
                 depth: int = 0,
                 origin: MatchResult = None):
        super().__init__()
        self.re = re
        self.start = start or 0
        self.stop = stop or maxsize
        self.depth = depth or 0
        self.origin = origin

    def __next(self, origin: MatchResult):
        return Repeat(self.re,
                      self.start,
                      self.stop,
                      depth=self.depth + 1,
                      origin=self.origin or origin)

    def match(self, m: MatchResult) -> MatchResult:
        reresult = self.re.match(m)
        before_stop = self.depth < self.stop

        if reresult.not_end() and reresult.matched() and before_stop:
            return self.__next(m).match(reresult)
        elif self.start <= self.depth <= self.stop:
            return reresult.current_ok()
        else:
            return (self.origin or m).bad()


class Choice(FnRegex):
    def __init__(self, left: FnRegex, right: FnRegex):
        super().__init__()
        self.left = left
        self.right = right

    def match(self, m: MatchResult) -> MatchResult:
        lm = self.left.match(m)

        if lm.matched():
            return lm
        else:
            return self.right.match(m)


class CharInterval(FnRegex):
    def __init__(self, first: chr, last: chr):
        super().__init__()
        self.first = first
        self.last = last

    def match(self, m: MatchResult) -> MatchResult:
        if self.first <= m.char() <= self.last:
            return m.ok()
        else:
            return m.bad()


class Char(FnRegex):
    def __init__(self, char: chr):
        super().__init__()
        self.char = char

    def __sub__(self, other: FnRegex) -> CharInterval:
        return CharInterval(self.char, other.char)

    def match(self, m: MatchResult) -> MatchResult:
        if m.not_end() and m.char() == self.char:
            return m.ok()
        else:
            return m.bad()


def match(fnrx: FnRegex, inp: str) -> MatchResult:
    return fnrx.match(MatchResult.input(inp))


def fullmatch(fnrx: FnRegex, inp: str) -> FullMatchResult:
    return FullMatchResult(match(fnrx, inp))


a = Char('a')
z = Char('z')
A = Char('A')
Z = Char('Z')
_0 = Char('0')
_9 = Char('9')
at = Char('@')
dot = Char('.')
_d = _0 - _9
_l = a - z
_U = A - Z
seq = a >> a
name = (A - Z | a - z | _0 - _9 | Char('_'))[:100]
email = name >> dot >> name >> at >> name >> dot >> name

if __name__ == '__main__':
    # import sys
    # sys.getrecursionlimit()
    # sys.setrecursionlimit(max)
    print(fullmatch(email, 'padget.pro@@gmail.com').matched())
