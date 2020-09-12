const merge = require("webpack-merge")
const config = require("fh-webpack-config")

module.exports = merge.smart(
  config.commonConfig,
  {
    entry: {
      main: "./main.js",
      admin: "./admin.js",
    },
  }
  // config.preactConfig,
  // config.chunkSplittingConfig
)
