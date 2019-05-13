const routes = require("express").Router();
const memoize = require("memoizee");

const getDila = require("../getDila");

const getTexteData = memoize((baseDILA, id, date) => getDila(baseDILA).getTexte({ id, date }), {
  promise: true
});

routes.get("/texte/:texteId", async (req, res) => {
  const date = new Date().toISOString().slice(0, 10);
  const texte = await getTexteData(req.baseDILA, req.params.texteId, date);
  res.json(texte);
});

module.exports = routes;
