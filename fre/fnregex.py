"""Le module fnregex permet de mettre en place
un mécanisme d'expression regulière non pas à
base de string comme classique, mais à base des
opérateurs python disponibles.
"""

from __future__ import annotations
from dataclasses import dataclass
from sys import maxsize
from typing import Callable


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


FnRegex = Callable[[MatchResult], MatchResult]


def seq(left: FnRegex, right: FnRegex) -> FnRegex:
    """ Un Sequence est une suite de FnRegex
    qui doivent toutes matcher pour être validé.
    """

    def apply(m: MatchResult):
        """Teste si le contenu de m match avec la sequence

        :param m: contenu à tester
        :return: un nouveau MatchResult
        """

        lresult = left(m)

        if lresult.matched():
            rresult = right(lresult)

            if rresult.matched():
                return rresult

        return m.bad()

    return apply


def repeat(re: FnRegex, start: int, stop: int, origin: MatchResult = None):
    """Un Repeat permet de mettre en place
    une répétition sur une même FnRegex. Elle
    peut être bornée par un min et un max.
    La valeur min doit être atteinte et la valeur
    max stop l'inspection
    """

    def __next(o: MatchResult):
        return repeat(re, start - 1, stop - 1, origin=origin or o)

    def apply(m: MatchResult) -> MatchResult:
        """Teste si le contenu de m match entre min
        et max fois la FnRegex répétée

        :param m: contenu à tester
        :return: un nouveau MatchResult
        """

        if stop is 0:
            return m.current_ok()
        else:
            reresult = re(m)

            if reresult.matched():
                return __next(m)(reresult)
            elif start <= 0 <= stop:
                return reresult.current_ok()
            else:
                return (origin or m).bad()

    return apply


def choice(left: FnRegex, right: FnRegex) -> FnRegex:
    """Choice permet de modéliser le complémentaire
    de la Sequence à savoir un choix parmi n FnRegex
    """

    def apply(m: MatchResult):
        """Teste si l'un des choix disponibles est correct

        :param m: contenu à tester
        :return: un nouveau MatchResult
        """

        lm = left(m)

        if lm.matched():
            return lm
        else:
            return right(m)

    def apply(m: MatchResult):
        lm = left(m)

    return apply


def charinterval(first: chr, last: chr) -> FnRegex:
    """Un CharInterval est un interval de deux
    FnRegex de type Char et permet donc de tester
    si un contenu est entre ces deux Chars
    """

    return lambda m: m.ok() \
        if m.not_end() and first <= m.char() <= last \
        else m.bad()


def char(c: chr) -> FnRegex:
    """Un Char représente le FnRegex le plus simple,
    le fait de tester un contenu par rapport à un
    unique caractère
    """

    return lambda m: m.ok() \
        if m.not_end() and m.char() == c \
        else m.bad()


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

    return fnrx(MatchResult.input(inp))


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
