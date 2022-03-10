module.exports = {
  pluginOptions: {
    quasar: {
      importStrategy: "kebab",
      rtlSupport: false,
    },
  },
  transpileDependencies: ["quasar"],
  devServer: {
    proxy: {
      "^/api": {
        target: "http://localhost:5588",
        pathRewrite: {
          pathRewrite: { "^/api": "/api" },
        },
      },
    },
    https: false,
    disableHostCheck: true,
  },
};
