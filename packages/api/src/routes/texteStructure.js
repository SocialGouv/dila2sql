const routes = require("express").Router();
const memoize = require("memoizee");
const getDila = require("../getDila");
const getStructure = require("../lib/getStructure");

const getSommaireData = memoize(
  (baseDILA, id, date, includeArticles, includeCalipsos) =>
    getDila(baseDILA).getSommaireTexte({
      id,
      date,
      includeArticles,
      includeCalipsos
    }),
  { promise: true }
);

routes.get("/texte/:texte/structure", async (req, res) => {
  const date = new Date().toISOString().slice(0, 10);
  const includeArticles = req.query.includeArticles === "true" || false;
  const includeCalipsos = req.query.includeCalipsos === "true" || false;
  const data = await getSommaireData(
    req.baseDILA,
    req.params.texte,
    date,
    includeArticles,
    includeCalipsos
  );
  res.json(getStructure(data));
});

module.exports = routes;
