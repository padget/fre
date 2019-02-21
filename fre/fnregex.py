"""Le module fnregex permet de mettre en place
un mécanisme d'expression regulière non pas à
base de string comme classique, mais à base des
opérateurs python disponibles.
"""

from __future__ import annotations
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

        return MatchResult(self.value, self.index + 1)

    def current_ok(self):
        """Construit un MatchResult ayant un résultat
        de matching à True mais restant sur son index
        de parcourt actuel

        :return: un nouveau MatchResult
        """

        return MatchResult(self.value, self.index)

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
    """Un FullMatchResult représente un résultat de
    matching sur l'ensemble d'un string, au contraire
    de MatchResult qui représente un résultat de match
    partiel.
    """

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
    """Un FnRegex est une interface permettant
    de définir ce qu'est une fonction regex. Elle
    oblige les implémentations à mettre en place
    la méthode
    match(self, m: MatchResult) -> MatchResult
    """

    def match(self, m: MatchResult) -> MatchResult:
        """match permet de dire si l'entrée m est correct
        vis à vis de la FnRegex qui est en cours d'analyse

        :param m: Entrée à faire matcher avec la FnRegex
        :return: Un nouveau MatchResult représentant le
                résultat du matching courant
        """

        pass


@dataclass(frozen=True)
class Sequence(FnRegex):
    """ Un Sequence est une suite de FnRegex
    qui doivent toutes matcher pour être validé.
    """

    left: FnRegex
    right: FnRegex

    def match(self, m: MatchResult) -> MatchResult:
        """Teste si le contenu de m match avec la sequence

        :param m: contenu à tester
        :return: un nouveau MatchResult
        """

        lresult = self.left.match(m)

        if lresult.matched():
            rresult = self.right.match(lresult)

            if rresult.matched():
                return rresult

        return m.bad()


class Repeat(FnRegex):
    """Un Repeat permet de mettre en place
    une répétition sur une même FnRegex. Elle
    peut être bornée par un min et un max.
    La valeur min doit être atteinte et la valeur
    max stop l'inspection
    """

    def __init__(self,
                 re: FnRegex,
                 start: int,
                 stop: int,
                 nb_match: int = 0,
                 origin: MatchResult = None):
        super().__init__()
        self.re = re
        self.start = start or 0
        self.stop = stop or maxsize
        self.nb_match = nb_match
        self.origin = origin

    def __next(self, origin: MatchResult):
        return Repeat(self.re,
                      self.start,
                      self.stop,
                      nb_match=self.nb_match + 1,
                      origin=self.origin or origin)

    def match(self, m: MatchResult) -> MatchResult:
        """Teste si le contenu de m match entre min
        et max fois la FnRegex répétée

        :param m: contenu à tester
        :return: un nouveau MatchResult
        """

        if self.nb_match == self.stop:
            return m.current_ok()
        else:
            reresult = self.re.match(m)

            if reresult.matched():
                return self.__next(m).match(reresult)
            elif self.start <= self.nb_match <= self.stop:
                return reresult.current_ok()
            else:
                return (self.origin or m).bad()


@dataclass(frozen=True)
class Choice(FnRegex):
    """Choice permet de modéliser le complémentaire
    de la Sequence à savoir un choix parmi n FnRegex
    """

    left: FnRegex
    right: FnRegex

    def match(self, m: MatchResult) -> MatchResult:
        """Teste si l'un des choix disponibles est correct

        :param m: contenu à tester
        :return: un nouveau MatchResult
        """

        lm = self.left.match(m)

        if lm.matched():
            return lm
        else:
            return self.right.match(m)


@dataclass(frozen=True)
class CharInterval(FnRegex):
    """Un CharInterval est un interval de deux
    FnRegex de type Char et permet donc de tester
    si un contenu est entre ces deux Chars
    """

    first: chr
    last: chr

    def match(self, m: MatchResult) -> MatchResult:
        """Teste si le contenu de m est entre les deux
        Char first et last

        :param m: contenu à tester
        :return: un nouveau MatchResult
        """

        if m.not_end() and self.first <= m.char() <= self.last:
            return m.ok()
        else:
            return m.bad()


@dataclass(frozen=True)
class Char(FnRegex):
    """Un Char représente le FnRegex le plus simple,
    le fait de tester un contenu par rapport à un
    unique caractère
    """
    char: chr

    def match(self, m: MatchResult) -> MatchResult:
        """Teste si le contenu de m correspond
        strictement au caractère attendu

        :param m: contenu à tester
        :return: un nouveau MatchResult
        """

        if m.not_end() and m.char() == self.char:
            return m.ok()
        else:
            return m.bad()


def match(fnrx: FnRegex, inp: str) -> MatchResult:
    """Fonction générale permettant de tester inp
    par rapport à le FnRegex fnrx passée en paramètre

    Un matching partiel de l'input est autorisé. Pour
    controler un matching total, il faut utiliser la
    méthode fullmatch

    :param fnrx: FnRegex portant le test
    :param inp: input à tester en fonction du FnRegex
    :return: un nouveau MatchResult témoignant du
            résultat final
    """

    return fnrx.match(MatchResult.input(inp))


def fullmatch(fnrx: FnRegex, inp: str) -> FullMatchResult:
    """Fonction générale permettant de tester inp
    par rapport à le FnRegex fnrx passée en paramètre

    Un matching total de l'input est exigé. Pour
    controler un matching partiel, il faut utiliser
    la méthode match

    :param fnrx: FnRegex portant le test
    :param inp: input à tester en fonction du FnRegex
    :return: un nouveau FullMatchResult témoignant du
            résultat final
    """

    return FullMatchResult(match(fnrx, inp))


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

    def match(self, m: MatchResult) -> MatchResult:
        """Execute le matching de la FnRegex wrappée

        :param m: MatchResult servant de point de départ
                  pour le matching
        :return: le résultat de l'appel ```fnrx.match(m)```
        """

        return self.fnrx.match(m)

    def __sub__(self, other: OperatorFnRegex) -> OperatorFnRegex:
        """Opérateur permettant de construire un
        CharInterval à partir de deux Char, le courant
        et l'other

        :param other: opérande de droite de l'opérateur
        :return: un nouveau CharInterval
        """

        return OperatorFnRegex(CharInterval(self.fnrx.char, other.fnrx.char))

    def __or__(self, other: OperatorFnRegex) -> OperatorFnRegex:
        """Construit un FnRegex de type Choice

        :param other: l'autre choix
        :return: un nouveau Choice
        """

        return OperatorFnRegex(Choice(self.fnrx, other.fnrx))

    def __getitem__(self, sl: slice):
        """Construit un FnRegex de type Repeat

        :param sl: les limites min et max du Repeat
        :return: un nouveau Repeat
        """

        if isinstance(sl, slice):
            start = sl.start
            stop = sl.stop
            return OperatorFnRegex(Repeat(self.fnrx, start, stop))
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

        return OperatorFnRegex(Sequence(self.fnrx, other.fnrx))


def op(fnrx: FnRegex) -> OperatorFnRegex:
    """Construit un OperatorFnRegex à partir
    d'un FnRegex

    :param fnrx: à wrapper dans un OperatorFnRegex
    :return: un nouveau OperatorFnRegex
    """

    return OperatorFnRegex(fnrx)
