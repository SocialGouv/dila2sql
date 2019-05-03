const { getStructure } = require("./getStructure");
const getConteneurData = require("./getConteneurData");
const { makeAst } = require("./utils");

const getConteneur = (knex, { id, date, includeChildren = false }) => {
  if (includeChildren) {
    return getStructure({ knex, date, maxDepth: 0, parentId: id }).then(async rows => ({
      type: "conteneur",
      data: await getConteneurData(knex, { id }),
      children: makeAst(rows, id)
    }));
  } else {
    return getConteneurData(knex, { id }).then(data => ({
      type: "conteneur",
      data
    }));
  }
};

module.exports = getConteneur;
