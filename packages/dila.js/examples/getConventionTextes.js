const dila = require("./dila");
const { JSONlog } = require("../src/utils");

dila
  .getConventionTextes({
    conteneurId: "KALICONT000005635691",
    typeTextes: "extensions",
    date: "2019-01-01"
  })
  .then(JSONlog)
  .catch(console.log)
  .then(dila.close);
