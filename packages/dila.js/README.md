# dila.js [![experimental](http://badges.github.io/stability-badges/dist/experimental.svg)](http://github.com/badges/stability-badges)

[![npm](https://img.shields.io/npm/v/dila.svg)](https://www.npmjs.com/package/dila)
![license](https://img.shields.io/npm/l/dila.svg)
[![github-issues](https://img.shields.io/github/issues/revolunet/dila.js.svg)](https://github.com/SocialGouv/dila2sql/issues)

[![nodei.co](https://nodei.co/npm/dila.png?downloads=true&downloadRank=true&stars=true)](https://www.npmjs.com/package/dila)

Une API NodeJS pour requêter les textes de loi bruts issus d'une base [dila2sql](https://github.com/SocialGouv/dila2sql)

Utilise [knex](https://github.com/tgriesser/knex/) pour exploiter les données d'une base et le standard [unist](https://github.com/syntax-tree/unist) pour représenter les textes sous forme d'arbre, de HTML, ou de markdown.

Par défaut l'API utilisateur utilise une base de données publique pour fournir les textes.

Vous pouvez utiliser votre propre base de données en montant votre base de données PostgreSQL avec [dila2sql](https://github.com/SocialGouv/dila2sql).

## Install

```sh
npm install dila
```

## Usage

Promise-based API

```js
const Dila = require("dila");

const dila = new Dila();

// liste des codes disponibles
dila.getCodesList().then(console.log);

// code du travail (~1min)
dila.getCode({ cid: "LEGITEXT000006072050", date: "2012-03-05" }).then(console.log);

// section d'un texte
dila.getSection({ id: "LEGISCTA000006132321", date: "2018-05-03" }).then(console.log);

// conversion en markdown
const markdown = require("dila.js/src/markdown");
dila
  .getCode({ cid: "LEGITEXT000006069414", date: "2012-03-05" })
  .then(markdown)
  .then(console.log);

// conversion en html
const html = require("dila.js/src/html");
legi
  .getCode({ cid: "LEGITEXT000006069414", date: "2012-03-05" })
  .then(html)
  .then(console.log);
```

Pour utiliser votre propres serveur PostgreSQL :

```
const legi = new Dila({
  client: "pg",
  connection: {
    host: "127.0.0.1",
    port: 5432,
    user: "user",
    password: "pass",
    database: "legi"
  },
  pool: { min: 0, max: 50 }
});
```

Plus d'exemples dans [./examples](./examples)

## Run Tests

```sh
jest
```

## Todo

- gestion dates/versions
- gestion textes type JORF, decrets...
