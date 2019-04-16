const dila = require("./dila");
const { JSONlog } = require("../src/utils");

// get code sommaire
dila
  .getSommaireConteneur({
    id: "KALICONT000005635807",
    date: "2019-05-01",
    includeArticles: true,
    includeCalipsos: true
  })
  .then(JSONlog)
  .catch(console.log)
  .then(dila.close);
