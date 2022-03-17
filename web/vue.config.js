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
      "^/socket": {
        target: "http://localhost:5588",
        pathRewrite: {
          pathRewrite: { "^/socket": "/socket" },
        },
      },
    },
    https: false,
    disableHostCheck: true,
  },
};
