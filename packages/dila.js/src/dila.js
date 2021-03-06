const knexRequire = require("knex");

const { getDefaultConfig } = require("./knexfile");

const dila = (knexConfig = null) => {
  const knex = knexRequire(knexConfig || getDefaultConfig());

  // tasty curry
  const knexify = module => params => module(knex, params);

  // the public API methods handlers will receive current knex connection as 1st arg
  return {
    getTexte: knexify(require("./getTexte")),
    getConteneur: knexify(require("./getConteneur")),
    getCodesList: knexify(require("./getCodesList")),
    getConteneursList: knexify(require("./getConteneursList")),
    getArticle: knexify(require("./getArticle")),
    getSection: knexify(require("./getSection")),
    getTetier: knexify(require("./getTetier")),
    getSommaireTexte: knexify(require("./getSommaire").getSommaireTexte),
    getSommaireConteneur: knexify(require("./getSommaire").getSommaireConteneur),
    getConventionTextes: knexify(require("./getConventionTextes")),
    close: () => knex && knex.destroy(),
    knex
  };
};

class Dila {
  constructor(knexConfig) {
    return dila(knexConfig);
  }
}

module.exports = Dila;
