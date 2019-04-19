const routes = require("express").Router();
const memoize = require("memoizee");
const map = require("unist-util-map");

const getDila = require("../getDila");

// extract basic text structure
const getStructure = tree =>
  map(tree, node =>
    Object.assign(
      {
        children: node.children,
        type: node.type,
        id: node.data && node.data.id,
        titre: node.data && node.data.titre,
        etat: node.data && node.data.etat
      },
      node.type === "article" ? { calipsos: node.data && node.data.calipsos } : {},
      node.type === "texte"
        ? {
            nature: node.data && node.data.nature,
            date_texte: node.data && node.data.date_texte,
            origine_publi: node.data && node.data.origine_publi
          }
        : {}
    )
  );

const getSommaireData = memoize(
  (baseDILA, id, date, includeArticles, includeCalipsos) =>
    getDila(baseDILA).getSommaireConteneur({
      id,
      date,
      includeArticles,
      includeCalipsos
    }),
  { promise: true }
);

routes.get("/conteneur/:conteneurId/structure", async (req, res) => {
  const date = new Date().toISOString().slice(0, 10);
  const includeArticles = req.query.includeArticles === "true" || false;
  const includeCalipsos = req.query.includeCalipsos === "true" || false;
  const data = await getSommaireData(
    req.baseDILA,
    req.params.conteneurId,
    date,
    includeArticles,
    includeCalipsos
  );
  res.json(getStructure(data));
});

module.exports = routes;
