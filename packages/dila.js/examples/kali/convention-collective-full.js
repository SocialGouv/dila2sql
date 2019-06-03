const dila = require("../dila");
const { JSONlog } = require("../../src/utils");

/*
renvoie la structure de base d'une convention collective et de tous ses textes attachés en JSON

ex: KALICONT000005635807: Convention collective nationale des salariés du particulier employeur du 24 novembre 1999.
*/

const flatify = arr => arr.reduce((a, c) => [...a, ...c], []);

dila
  // récupère le conteneur principal
  .getConteneur({ id: "KALICONT000005635807", date: "2019-01-01" })
  // récupère le texte du conteneur principal
  .then(({ data }) => dila.getTexte({ id: data.texte_de_base, date: "2019-01-01" }))
  .then(texte =>
    // récupères tous les textes attachés
    Promise.all(
      ["extensions", "attaches", "salaires"].map(typeTextes =>
        dila
          .getConventionTextes({
            conteneurId: "KALICONT000005635807",
            typeTextes,
            date: "2019-01-01"
          })
          .then(data =>
            // recupère la structure de chaque texte attaché
            Promise.all(
              data.textes.map(texte => dila.getTexte({ id: texte.id, date: "2019-01-01" }))
            )
          )
      )
    )
      .then(flatify)
      .then(attaches => ({
        id: "KALICONT000005635807",
        date: "2019-01-01",
        base: texte,
        attaches
      }))
  )

  .then(JSONlog)
  .catch(console.log)
  .then(dila.close);
