var execSync = require("child_process").execSync;

module.exports = async function() {
  execSync(`${__dirname}/seeds/setup_db.sh`);
};
