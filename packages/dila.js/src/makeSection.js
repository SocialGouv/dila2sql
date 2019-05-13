const { cleanData } = require("./utils");

const makeSection = data => ({
  type: "section",
  data: cleanData({
    ...data,
    titre: data.titre_ta && data.titre_ta
  })
});

module.exports = makeSection;
