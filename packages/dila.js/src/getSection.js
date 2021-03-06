const { getStructure } = require("./getStructure");
const getSectionData = require("./getSectionData");
const { makeAst } = require("./utils");

const getSection = async (knex, { parentId: cid, id = null, date, maxDepth = 2 }) => {
  if (!/[A-Z]{4}SCTA\d+/.test(id)) {
    throw new Error("not a valid section id");
  }
  return getStructure({ knex, parentId: id || cid, date, section: id, maxDepth }).then(
    async rows => ({
      // make the final AST-like structure
      type: "section",
      data: await getSectionData(knex, { id }),
      children: makeAst(rows, id)
    })
  );
};

module.exports = getSection;
