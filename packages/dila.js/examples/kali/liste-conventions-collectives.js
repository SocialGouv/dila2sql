const dila = require("../dila");
const { JSONlog } = require("../../src/utils");

/*
liste les conventions actives en JSON

actives = selon le fichier publié sur le site de la DGT à une url type  https://travail-emploi.gouv.fr/IMG/xls/idccjuin19.xls
*/

dila
  .getConteneursList({ nature: "IDCC", active: true })
  .then(JSONlog)
  .catch(console.log)
  .then(dila.close);
