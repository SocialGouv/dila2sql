# dila2sql

![DILA2SQL Logo](https://i.imgur.com/wS0w4lO.png)

Ce mono-repository contient trois packages:

- `dila2sql`: générer des bases SQL à partir des exports publiés au format XML par la [DILA (Direction de l’information légale et administrative)][dila].
- `dilajs`: librairie NodeJS qui permet d'accéder à une base PostgreSQL générée par `dila2sql`
- `api`: API Express qui expose la base générée en utilisant `dila.js`

Le package `dila2sql` est un fork du projet [`legi.py`][legi.py] créé par [Legilibre][legilibre] et [@Changaco][changaco].

Les packages `api` et `dilajs` ont été initialement créés par [@revolunet][revolunet] dans le cadre du projet [`legixplore`][legixplore].
Nous les avons ensuite migrés dans ce mono-repository pour des raisons pratiques et logiques.

## Utilisation avec Docker

```bash
# lancer tous les containers
docker-compose up -d

# créer la base de donnée
docker-compose exec db psql -U dila2sql -c "CREATE DATABASE kali"

# lancer le téléchargement des dumps XML originaux depuis legifrance
docker-compose run dila2sql python -m dila2sql.download --base KALI

# lancer l'import de ces dumps dans la base Postgres
docker-compose run dila2sql python -m dila2sql.importer --base KALI --raw postgresql://dila2sql:dila2sql@db/kali
```

Ce processus peut être décliné pour les bases LEGI ou JORF.

## Développer sans Docker

À la racine du projet, lancez `yarn install`. Puis :

```sh
cd packages/api
yarn dev
```

`yarn` fera alors le lien entre les différents packages locaux : principalement l'API qui utilise le package `dila.js`.
Les modifications que vous ferez en local sur le package de l'API ou le package `dila.js` seront automatiquement prises en compte grâce à `nodemon` qui redémarre le serveur lors d'un changement de fichier.

Vous pouvez aussi vous développer indépendamment sur `dila.js` en vous plaçant dans `packages/dila.js` et en lançant les exemples ou les tests :

```sh
cd packages/dila.js
DB_URL=postgresql://localhost/kali node examples/getSommaireConteneur.js
```

## Développer avec Docker

⚠️ Il est conseillé de développer sans Docker pour plus de simplicité et avoir un live reload du code simple.

Lancez les commandes en montant le code local vers le chemin du code applicatif dans le container pour utiliser le code local plutôt que celui de l'image buildée.

```bash
# Ex: lancer le téléchargement des dumps
docker-compose run -v $PWD/packages/dila2sql:/app dila2sql python -m dila2sql.download --base KALI
```

## Contribuer

Les _Pull Requests_ sont bienvenues.

Les [autres bases de la DILA][dila-bases] sont disponibles dans des dumps XML similaires, il devrait donc être relativement aisé d'adapter `dila2sql` pour les supporter.

## Projets connexes

- http://github.com/Legilibre
- https://framagit.org/parlement-ouvert
- http://github.com/regardscitoyens
- https://framagit.org/tricoteuses

## Licence

[CC0 Public Domain Dedication](http://creativecommons.org/publicdomain/zero/1.0/)

[dila]: http://www.dila.premier-ministre.gouv.fr/
[legi.py]: https://github.com/Legilibre/legi.py/
[legilibre]: https://github.com/Legilibre
[changaco]: https://github.com/Changaco
[revolunet]: https://github.com/revolunet
[legixplore]: https://github.com/SocialGouv/legixplore/
[dila-bases]: https://www.dila.premier-ministre.gouv.fr/repertoire-des-informations-publiques/les-donnees-juridiques
