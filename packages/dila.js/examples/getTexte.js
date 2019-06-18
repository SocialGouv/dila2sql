const dila = require("./dila");
const { JSONlog } = require("../src/utils");

// get code structure
dila
  .getTexte({ id: "KALITEXT000005672639", date: "2019-06-18" })
  .then(JSONlog)
  .catch(console.log)
  .then(dila.close);
