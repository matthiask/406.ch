Title: Using Django with Webpack – 2024 edition
Date: 2024-03-21
Categories: Django, Programming
Draft: remove-this-to-publish

In 2018 I published a post outlining [our approach to configuring Django and
Webpack to work well
together](https://406.ch/writing/our-approach-to-configuring-django-webpack-and-manifeststaticfilesstorage/).
This post is very outdated, and it's about time I published an updated version.

I have looked into using other bundlers, but have had limited success switching
existing projects to more modern build stacks. I'm very much looking forward to
using a faster CSS and JavaScript build pipeline, but for now I'm still a happy
Webpack user. It just works well, and supports hot module reloading (especially
important for me is CSS HMR support), PostCSS, and transpiling JavaScript for
older browsers.

In the past I have used the bundle tracker plugins for Webpack and Django. On
the Webpack side, a plugin spit out a JSON file containing paths, on the Django
side the JSON file was parsed to generate the needed `<link>` and `<script>`
tags.

These days I'm using the
[HtmlWebpackPlugin](https://webpack.js.org/plugins/html-webpack-plugin/) to
generate a small HTML snippet which is more or less loaded 1:1 into the
`<head>` of my sites.

## Webpack configuration

The Webpack configuration basically sets up PostCSS with autoprefixer (that's
always a great idea), mini-css to split out CSS into its own file, and babel to
transpile JavaScript.

It's a lot. Of course you could use one of the wrappers which make it a bit
more plug and play, but you lose a few of the features, as always. The most
important aspect is that Webpack respectively webpack-dev-server also proxies
the HTTP requests it doesn't handle itself to the Django backend. This allows
for a great development experience when using external testing devices, because
those automatically work: Instead of connecting to `http://localhost:8000` you
connect to `http://192.168....:8000` from your network. Everything works
without having to do anything else, it's great. As an aside, this was one of
the features I couldn't replicate with other toolchains and that sucks a lot.

    :::javascript
    module.exports = (env, argv) => {
      const PRODUCTION = argv.mode === "production"

      return {
        mode: PRODUCTION ? "production" : "development",
        bail: PRODUCTION,
        devtool: PRODUCTION ? "source-map" : "eval-source-map",
        context: path.join(cwd, "frontend"),
        entry: { main: './main.js' },
        output: {
          clean: { keep: /\.html$/ },
          path: path.join(cwd, "static"),
          publicPath: "/static/",
          filename: '[name].js',
          assetModuleFilename: '_/[name].[hash][ext][query]'
        },
        plugins: [
          new MiniCssExtractPlugin({
            filename: PRODUCTION ? "[name].[contenthash].css" : "[name].css",
          }),
          new HtmlWebpackPlugin({
            filename: `${PRODUCTION ? "" : "debug."}[name].html`,
            templateContent: "<head></head>",
          }),
        ],
        devServer: {
          host: '0.0.0.0',
          hot: true,
          port: 8000,
          allowedHosts: 'all',
          client: { overlay: { errors: true, warnings: false, runtimeErrors: true } },
          devMiddleware: {
            headers: { "access-control-allow-origin": "*" },
            index: true,
            writeToDisk: (path) => /\.html$/.test(path),
          },
          proxy: {
            context: () => true,
            target: 'http://127.0.0.1:12345'
          }
        },
        module: {
          rules: [
            {
              test: /\.(png|woff2?|svg|eot|ttf|otf|gif|jpe?g|mp3|wav)$/i,
              type: "asset",
              parser: { dataUrlCondition: { maxSize: 512 /* bytes */ } },
            },
            {
              test: /\.css$/i,
              use: [
                PRODUCTION ? MiniCssExtractPlugin.loader : { loader: "style-loader" },
                { loader: "css-loader" },
                { loader: "postcss-loader", options: { postcssOptions: { ["autoprefixer"] } } },
              ],
            },
            {
              test: /\.m?js$/i,
              exclude: /(node_modules)/,
              use: {
                loader: "babel-loader",
                options: {
                  cacheDirectory: true,
                  presets: [
                    [
                      "@babel/preset-env",
                      { useBuiltIns: "usage", corejs: "3.33", targets: "defaults" },
                    ],
                  ],
                },
              },
            },
          ],
        },
      }
    }

I'm definitely not keeping that much JavaScript up to date in each project though. That's why most of the code above is packaged in a small library which is automatically copied into each project by our tooling. The current state is [`webpack.library.js`](https://github.com/feinheit/fh-fablib/blob/42a70827fad7b511b02e44060a66772c718751de/fh_fablib/dotfiles/webpack.library.js), and when using it, the `webpack.config.js` file suddenly looks much nicer and more understandable:

    :::javascript
    module.exports = (env, argv) => {
      const { base, devServer, assetRule, postcssRule, babelRule } =
        require("./webpack.library.js")(argv.mode === "production")

      return {
        ...base,
        devServer: devServer({ backendPort: env.backend }),
        module: {
          rules: [
            assetRule(),
            postcssRule({ plugins: ["autoprefixer"] }),
            babelRule(),
          ],
        },
      }
    }

## Django side

The Django side consists of a template tags which knows how to locate the HTML file spit out by the Webpack plugin; all it has to do is strip the surrounding `<head>` tags from the HTML and remove the rest as-is:

    :::python
    from functools import cache
    from django import template
    from django.conf import settings
    from django.utils.html import mark_safe

    register = template.Library()

    def webpack_assets(entry):
        debug = "debug." if settings.DEBUG else ""
        html = (settings.STATIC_ROOT / f"{debug}{entry}.html").read_text()
        return mark_safe(html.strip().removeprefix("<head>").removesuffix("</head>"))

    if not settings.DEBUG:
        webpack_assets = cache(webpack_assets)
    register.simple_tag(webpack_assets)

The template tag is used in templates as:

    :::html+django
    {% load webpack_assets %}{% webpack_assets 'main' %}

That's it.

## Deployment

To deploy the frontend code I follow these steps:

- I run `webpack --mode production`
- I `rsync` the contents of `static` into the server's `static` folder
- I run `manage.py collectstatic --noinput` on the server

The same happens when building a container image of course.
