const { cleanData } = require("./utils");

const makeTetier = data => ({
  type: "tetier",
  data: cleanData({
    ...data,
    titre: data.titre_tm && data.titre_tm
  })
});

module.exports = makeTetier;
