# Functionnal Regular Expression : fre

**fre** permet d'utiliser les expressions régulières directement en python sans 
passer par les strings.

## Motivation

Utiliser les expressions régulières fait partie des choses basiques en 
ingéniérie logicielle et la plupart du temps cela se fait au travers de strings
qui sont parsées puis utilisées pour effectuer le matching avec d'autres 
chaines.

C'est pourquoi il y a **fre** qui permet de coder les expressions régulières 
directement en python sans phase de précompilation. On a donc un gain de 
performance à l'exécution. 

## Features

**fre** permet d'écrire les expressions régulières directement en python, soit
de manière purement fonctionnelle, soit avec des opérateurs.

#### Un exemple fonctionnel

```python
from fre.fnregex import charinterval, char

def match_lower(c: chr) -> bool:
    lower = charinterval(char('a'), char('z')) # utilisation de fonctions
    return lower(c).matched()
```

#### Le même avec les opérateurs

```python
from fre.opregex import a, z

def match_lower(c: chr) -> bool:
    lower = a - z # utilisation de l'opérateur d'interval
    return lower(c).matched()
```


**fre** expose deux fonctions principales : 

```python
def match(fnrx: FnRegex, inp: str) -> MatchResult:
    ...
```
```python
def fullmatch(fnrx: FnRegex, inp: str) -> FullMatchResult:
    ...
```

Ces deux fonctions prennent en premier paramètre une FnRegex construite soit de
manière fonctionnelle soit avec les opérateurs et en second paramètre la string
dont on veut savoir si la valeur correspond ou pas avec l'expression régulière. 

`fullmatch` au contraire de `match` demande à ce que la totalité de la string soit
en correspondance avec l'expression régulière. Alors que `match` elle ne demande
que le début soit correspondant. 

## Installation

#### Pypi

```bash
pip install fre
``` 

## Contribution

## Licence

**fre** est sous [licence MIT](LICENSE) 




