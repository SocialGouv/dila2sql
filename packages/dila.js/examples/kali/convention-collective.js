const dila = require("../dila");
const html = require("../../src/html");

/*
renvoie le texte de base d'une convention collective en HTML

ex: KALICONT000005635807: Convention collective nationale des salariés du particulier employeur du 24 novembre 1999.
*/

dila
  .getConteneur({ id: "KALICONT000005635807", date: "2019-01-01" })
  .then(({ data }) => dila.getTexte({ id: data.texte_de_base, date: "2019-01-01" }))
  .then(html)
  .then(console.log)
  .catch(console.log)
  .then(dila.close);

