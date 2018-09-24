/* global __dirname, process */
var path = require('path')
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')
var ExtractTextPlugin = require('extract-text-webpack-plugin')
var CleanWebpackPlugin = require('clean-webpack-plugin')

var HOST = process.env.HOST || '127.0.0.1'
var DEBUG = process.env.NODE_ENV !== 'production'
var HTTPS = !!process.env.HTTPS

function cssLoader(firstLoader) {
  return ExtractTextPlugin.extract({
    fallback: 'style-loader',
    use: ['css-loader?sourceMap', 'postcss-loader?sourceMap'].concat(
      firstLoader || []
    ),
  })
}

module.exports = {
  context: path.join(__dirname, 'mkweb', 'static', 'mkweb'),
  devtool: DEBUG ? 'eval' : 'source-map',
  entry: {
    main: './main.js',
    admin: './admin.js',
  },
  output: {
    path: path.resolve('./static/mkweb/'),
    publicPath: DEBUG
      ? 'http' + (HTTPS ? 's' : '') + '://' + HOST + ':4000/'
      : '/static/mkweb/',
    filename: '[name]-[hash].js',
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: [
          {
            loader: 'babel-loader',
            options: {
              presets: [['es2015', {modules: false}]],
              cacheDirectory: path.resolve(__dirname, 'tmp'),
            },
          },
        ],
      },
      {
        test: /\.css$/,
        use: cssLoader(),
      },
      {
        test: /\.scss$/,
        use: cssLoader({
          loader: 'sass-loader',
          options: {
            includePaths: [path.resolve(path.join(__dirname, 'node_modules'))],
            outputStyle: 'expanded',
            sourceMap: true,
          },
        }),
      },
      {
        test: /\.less$/,
        use: cssLoader('less-loader'),
      },
      {
        test: /\.(png|woff|woff2|svg|eot|ttf|gif|jpe?g)$/,
        use: [
          {
            loader: 'url-loader',
            options: {
              limit: 1000,
              // ManifestStaticFilesStorage reuse.
              name: '[path][name].[md5:hash:hex:12].[ext]',
              // No need to emit files in production, collectstatic does it.
              emitFile: DEBUG,
            },
          },
        ],
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
    modules: ['mkweb/static/mkweb/', 'node_modules'],
    alias: {},
  },
  plugins: [
    new CleanWebpackPlugin([path.resolve('./static/mkweb/')]),
    new ExtractTextPlugin({
      filename: '[name]-[hash].css',
      disable: DEBUG,
      allChunks: true,
    }),
    new BundleTracker({
      filename: './static/webpack-stats-' + (DEBUG ? 'dev' : 'prod') + '.json',
    }),
    DEBUG ? new webpack.NamedModulesPlugin() : null,
  ].filter(function(el) {
    return !!el
  }),
  devServer: {
    contentBase: false,
    inline: true,
    quiet: false,
    https: HTTPS,
    disableHostCheck: true,
    headers: {'Access-Control-Allow-Origin': '*'},
  },
  performance: {
    // No point warning in development, since HMR / CSS bundling blows up
    // the asset / entrypoint size anyway.
    hints: DEBUG ? false : 'warning',
  },
}
