const { cleanData } = require("./utils");

const makeArticle = data => ({
  type: "article",
  data: cleanData({
    ...data,
    titre: ["Article", data.num, data.titre].filter(e => e).join(" ")
  })
});

module.exports = makeArticle;
