module.exports = (env, argv) => {
  const PRODUCTION = argv.mode === "production"
  const {
    base,
    devServer,
    assetRule,
    postcssRule,
    babelRule,
    truthy,
    miniCssExtractPlugin,
    htmlSingleChunkPlugin,
    htmlInlineScriptPlugin,
    noSplitting,
  } = require("./webpack.library.js")(PRODUCTION)

  const entry = {
    main: "./main.js",
    admin: "./admin.js",
  }

  return {
    ...base,
    ...noSplitting,
    entry,
    devServer: devServer({ backendPort: env.backend }),
    module: {
      rules: [
        assetRule(),
        postcssRule({
          plugins: ["postcss-nested", "autoprefixer"],
        }),
        babelRule(),
      ],
    },
    plugins: truthy(
      miniCssExtractPlugin(),
      htmlSingleChunkPlugin("main"),
      htmlSingleChunkPlugin("admin"),
      htmlInlineScriptPlugin(),
    ),
  }
}
