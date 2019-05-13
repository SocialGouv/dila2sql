const routes = require("express").Router();
const memoize = require("memoizee");
const getDila = require("../getDila");

const memoizedGetConventionTextes = memoize(
  (baseDILA, conteneurId, typeTextes, date) =>
    getDila(baseDILA).getConventionTextes({ conteneurId, typeTextes, date }),
  { promise: true }
);
routes.get("/conteneur/:conteneurId/textes/:typeTextes", async (req, res) => {
  const date = new Date().toISOString().slice(0, 10);
  const textes = await memoizedGetConventionTextes(
    req.baseDILA,
    req.params.conteneurId,
    req.params.typeTextes,
    date
  );
  res.json(textes);
});

module.exports = routes;
