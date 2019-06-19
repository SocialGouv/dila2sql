const dila = require("./dila");
const { JSONlog } = require("../src/utils");

dila
  .getConventionTextes({
    conteneurId: "KALICONT000005635325",
    typeTextes: "base",
    date: "2019-01-01"
  })
  .then(JSONlog)
  .catch(console.log)
  .then(dila.close);
