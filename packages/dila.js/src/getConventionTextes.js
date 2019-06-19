const { getSommaireFilters } = require("./getStructure");

const TypesToTmTitre = {
  base: "Texte de base",
  extensions: "Textes Extensions",
  attaches: "Textes Attachés",
  salaires: "Textes Salaires"
};

const getConventionTextes = async (knex, { conteneurId, typeTextes, date }) => {
  const tetiersSql = `
    SELECT tetiers.*
    FROM sommaires
    LEFT JOIN tetiers ON tetiers.id = sommaires.element
    WHERE ${getSommaireFilters(date)}
    AND sommaires.parent = '${conteneurId}'
    AND tetiers.titre_tm = '${TypesToTmTitre[typeTextes]}'
  `;
  const tetiers = await knex.raw(tetiersSql).then(res => res.rows);
  if (tetiers.length == 0) {
    return { textes: [] };
  }
  const tetierId = tetiers[0].id;
  const textesSql = `
    SELECT textes_versions.*
    FROM sommaires
    LEFT JOIN textes_versions ON textes_versions.id = sommaires.element
    WHERE ${getSommaireFilters(date)}
    AND sommaires.parent = '${tetierId}'
    AND textes_versions.id IS NOT NULL
  `;
  const textes = await knex.raw(textesSql).then(res => res.rows);
  return { textes };
};

module.exports = getConventionTextes;
