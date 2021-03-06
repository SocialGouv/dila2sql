# dila2sql

Ce projet permet de générer des bases SQL à partir des exports publiés au format XML par la [DILA (Direction de l’information légale et administrative)][dila].

`dila2sql` est un fork du projet [`legi.py`][legi.py] créé par [Legilibre][legilibre] et [@Changaco][changaco].

Les bases de la DILA supportées sont :
- [LEGI][legi-data] : Codes, lois et règlements consolidés
- [KALI][kali-data] : Conventions collectives nationales
- [JORF][jorf-data] : Textes publiés au Journal officiel de la République française

Le projet supporte en sortie les formats PostgreSQL et SQLite.

## Fonctionnement

- téléchargement incrémental des archives XML
- création/migration de la base SQL
- parcours incrémental des archives et modifications dans la base SQL
- réparation des erreurs simples et amélioration (liens)
- nettoyage des données textuelles (normalisation des titres, fautes de français)
- détection d'anomalies

## Utilisation Locale

Voici quelques informations pour lancer vous même le projet sur votre machine, avec ou sans Docker

> 💡 Le premier lancement du projet peut prendre plusieurs heures selon votre matériel/connexion.

### Utilisation sans Docker

Le projet fonctionne uniquement avec Python 3.7+.

Installez [libarchive][libarchive] : `sudo apt-get install libarchive13` sur Debian/Ubuntu ou bien `brew install libarchive` sur Mac OS X.

Puis installez les dépendences Python :

    pip install -r requirements.txt

Cette commande lance le téléchargement incrémental des archives XML de la base LEGI et les sauvegarde dans `./data` :

    python -m dila2sql.runner --run-only downloader --base LEGI --dumps-dir ./data

Cette commande parcourt incrémentalement les nouvelles archives de la base LEGI présentes dans `./data` et crée (ou met à jour) une base de données SQLite stockée dans `./data/LEGI.sqlite`.

    python -m dila2sql.runner --run-only importer --base LEGI --db-url sqlite:///LEGI.sqlite --dumps-dir ./data

Commande équivalente pour la base KALI et une sortie Postgres :

    python -m dila2sql.runner --run-only importer --base KALI --raw --db-url postgresql://dila2sql:dilamite@localhost/kali --dumps-dir ./data

Pour lancer les tests il suffit de lancer `tox`

La configuration passe par un fichier de variables d'environnement, vous pouvez copier le template : `cp .env.sample .env`

### Avec Docker

Une image Docker `socialgouv/dila2sql` est hébergée sur DockerHub par l'[Incubateur des Ministères Sociaux][incubateur].

Vous pouvez aussi builder l'image Docker localement avec la commande suivante :

    docker build -t dila2sql .

Vous pouvez alors lancer toutes les commandes précédemment mentionnées en local sous cette forme :

    docker run --rm -t -v $PWD/data:/data socialgouv/dila2sql COMMANDE

Vous pouvez aussi développer dans l'image Docker en ajoutant `-v $PWD:/app` au lancement du container, le code utilisé sera alors celui de votre répertoire local.

Vous pouvez aussi lancer les tests dans l'image Docker grâce à cette commande :

    docker run --rm -t -v $PWD/data:/data socialgouv/dila2sql tox


### Parallélisme

Par défaut, le traitement des grosses archives est réparti sur plusieurs process.
La librairie utilise un [`ProcessPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#processpoolexecutor) qui infère automatiquement un nombre de process adaptés au contexte d'exécution.
Vous pouvez aussi configurer explicitement via la variable d'environnement `DILA2SQL_MAX_PROCESSES` (une valeur de 1 désactive la parallélisation).

## Problèmes libarchive avec Mac OS X

sur Mac OS X, il vous faudra aussi probablement exporter la variable `LD_LIBRARY_PATH` à cause de ce [bug connu][libarchive-bug].
Par exemple :

```sh
# ~/.bashrc
export LIBARCHIVE=/usr/local/Cellar/libarchive/3.3.3/lib/libarchive.13.dylib
```

De même en cas de problème lors du lancement des tests, essayez avec cette commande:

    TOX_TESTENV_PASSENV=LIBARCHIVE tox

## Différences par rapport à legi.py

- Support de plusieurs bases de la DILA en entrée
- Support de plusieurs bases SQL en sortie grâce à [peewee](http://docs.peewee-orm.com/en/latest/)
- Parallélisation des téléchargements
- Image Docker optionnelle pour isoler l'environnement


[dila]: http://www.dila.premier-ministre.gouv.fr/
[legi.py]: https://github.com/Legilibre/legi.py/
[legilibre]: https://github.com/Legilibre
[changaco]: https://github.com/Changaco
[legi-data]: https://www.data.gouv.fr/fr/datasets/legi-codes-lois-et-reglements-consolides/
[kali-data]: https://www.data.gouv.fr/fr/datasets/kali-conventions-collectives-nationales/
[jorf-data]: https://www.data.gouv.fr/fr/datasets/jorf-les-donnees-de-l-edition-lois-et-decrets-du-journal-officiel/
[incubateur]: https://github.com/socialgouv
[legi-sqlite]: https://dila2sql.num.social.gouv.fr/exports/sqlite/LEGI.sqlite
[legi-postgres]: https://dila2sql.num.social.gouv.fr/exports/postgres/LEGI.sql
[kali-sqlite]: https://dila2sql.num.social.gouv.fr/exports/sqlite/KALI.sqlite
[kali-postgres]: https://dila2sql.num.social.gouv.fr/exports/postgres/KALI.sql
[jorf-sqlite]: https://dila2sql.num.social.gouv.fr/exports/sqlite/JORF.sqlite
[jorf-postgres]: https://dila2sql.num.social.gouv.fr/exports/postgres/JORF.sql
[libarchive]: http://libarchive.org/
[libarchive-bug]: https://github.com/dsoprea/PyEasyArchive#notes
