const { createProxyMiddleware } = require("http-proxy-middleware");

// Forward API calls from the CRA dev server to the Docker proxy (https://localhost)
const DEFAULT_TARGET = "https://localhost";

module.exports = function setupProxy(app) {
  const target = process.env.OPENELIS_PROXY_TARGET || DEFAULT_TARGET;

  app.use(
    "/api/OpenELIS-Global",
    createProxyMiddleware({
      target,
      changeOrigin: true,
      secure: false, // allow the self-signed cert from docker-compose proxy
      logLevel: "warn",
    }),
  );
};
