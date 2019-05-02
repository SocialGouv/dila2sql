const map = require("unist-util-map");

// extract basic text structure
const getStructure = tree =>
  map(tree, node =>
    Object.assign(
      {
        children: node.children,
        type: node.type,
        id: node.data && node.data.id,
        titre: node.data && node.data.titre,
        etat: node.data && node.data.etat,
        titrefull: node.data && node.data.titrefull
      },
      node.type === "article" ? { calipsos: node.data && node.data.calipsos } : {},
      node.type === "texte"
        ? {
            nature: node.data && node.data.nature,
            date_texte: node.data && node.data.date_texte,
            origine_publi: node.data && node.data.origine_publi
          }
        : {}
    )
  );

module.exports = getStructure;
