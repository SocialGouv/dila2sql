## Installation

legi.py nécessite [`libarchive`][libarchive] ainsi que les modules python listés
dans `requirements.txt`. Tout est compatible avec python 2 et 3.

### Ubuntu

    sudo apt-get install libarchive13 python-lxml python-pip
    sudo pip install -r requirements.txt

## Utilisation

La première étape est de télécharger les archives LEGI depuis
`ftp://legi:open1234@ftp2.journal-officiel.gouv.fr/`:

    wget -c -N --no-remove-listing -nH 'ftp://legi:open1234@ftp2.journal-officiel.gouv.fr/*legi_*'

La deuxième étape est la conversion des archives en base SQLite:

    python -m legi.tar2sqlite legi.sqlite chemin/du/dossier/contenant/les/archives [--anomalies] [--anomalies-dir=.]

La taille du fichier SQLite créé est environ 3,3Go (en décembre 2016).

Vous pouvez lancer ce script régulièrement pour maintenir votre base de données
à jour, il saute automatiquement les archives qu'il a déjà traité. En général la
DILA publie une nouvelle archive chaque jour sauf pendant le weekend.

Le module `anomalies` est conçu pour détecter les incohérences dans les données
afin de les signaler à la DILA. L'option `--anomalies` de `tar2sqlite` génère
une liste d'anomalies après chaque archive traitée, l'intérêt étant de voir
l'évolution de la cohérence de la base dans le temps. Si l'historique ne vous
intéresse pas vous pouvez lancer la détection d'anomalies séparément après
`tar2sqlite` pour obtenir une seule liste:

    python -m legi.anomalies legi.sqlite

## Licence

[CC0 Public Domain Dedication](http://creativecommons.org/publicdomain/zero/1.0/)

## Historique du projet

Fin juin 2014 la [base de données LEGI][legi] contenant toutes les lois
françaises en vigueur a été libéré en Open Data. J'ai immédiatement [commencé le
travail][tweet] pour la convertir dans d'autres formats. Malheureusement,
distrait par d'autres choses à faire et un peu découragé par la structure
médiocre des données j'avais temporairement laissé le projet de côté.

Suite à [un billet de blog qui a fait du bruit][korben] j'ai découvert que
d'autres projets similaires sont apparus entre temps:

- [Seb35/Archeo-Lex](https://github.com/Seb35/Archeo-Lex/)
- [steeve/france.code-civil](https://github.com/steeve/france.code-civil)

ce qui m'a poussé à réouvrir, nettoyer et publier mon code.


[libarchive]: http://libarchive.org/
[legi]: https://www.data.gouv.fr/fr/datasets/legi-codes-lois-et-reglements-consolides/
[tweet]: https://twitter.com/Changaco/statuses/484674913954172929
[korben]: http://korben.info/10-etapes-pour-pirater-la-france.html
