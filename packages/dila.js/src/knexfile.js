const url = require("url");

const parseDbUrl = (dbUrl) => {
  const parsed = url.parse(dbUrl);
  const [user, password] = (parsed.auth || "").split(":");
  return {
    client: "pg",
    version: "9.6",
    connection: {
      host: parsed.hostname,
      port: parsed.port || 5432,
      user: user,
      password: password,
      database: parsed.path.substr(1) // starts with /
    },
    pool: {
      min: 0,
      max: 5
    }
  };
};

const getDefaultConfig = () => {
  if (process && process.env && process.env.DB_URL) {
    return parseDbUrl(process.env.DB_URL);
  } else {
    throw new Error("missing DB_URL env var pointing to a PostgreSQL generated with dila2sql");
  }
};

const getTestConfig = () => {
  if (process && process.env && process.env.TEST_DB_URL) {
    return parseDbUrl(process.env.TEST_DB_URL);
  } else {
    return parseDbUrl("postgresql://localhost/dila2sql_test");
  }
};

module.exports = { getDefaultConfig, getTestConfig };
