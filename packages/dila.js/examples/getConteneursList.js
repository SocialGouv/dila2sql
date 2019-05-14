const dila = require("./dila");
const { JSONlog } = require("../src/utils");

// get code sommaire
dila
  .getConteneursList({ nature: "IDCC", active: true })
  .then(JSONlog)
  .catch(console.log)
  .then(dila.close);
