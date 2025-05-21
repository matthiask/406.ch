Title: How I'm bundling frontend assets these days
Categories:
Draft: remove-this-to-publish

# How I'm bundling frontend assets these days

I last wrote about configuring Django with bundlers in 2018: [Our approach to configuring Django, Webpack and ManifestStaticFilesStorage](https://406.ch/writing/our-approach-to-configuring-django-webpack-and-manifeststaticfilesstorage/). An update has been a long time coming.

[We](https://feinheit.ch/) have looked at many different bundlers or at not using a bundler at all. In the end, the flexibility, speed and trustworthiness of rspack won me over.

Configuring rspack from scratch is no joke, that's why tools such as [rsbuild](https://rsbuild.dev/) exist. We already have a reusable library of configuration snippets for webpack and moving that library over to rspack was straightforward.

The high-level overview is:

- Frontend assets live in their own folder, `frontend/`.
- The `rspack.config.js` configuration is in the root folder of the project.
- The frontend is transpiled and bundled directly into `static/` for production and into `tmp/` during development.
- We use the HTML plugin of rspack to emit snippets containing `<link>` and `<script>` tags. The HTML snippet is included as-is.

During development:

- We use the dev server of rspack/node to handle `127.0.0.1:8000`. This server handles requests for frontend assets and the websocket for hot module reloading and proxies everything else to the Django backend running on a different (random) port.

During deployment:

- The assets are added to `static/` and rsynced to the server or added to the container separately from the standard `./manage.py collectstatic --noinput`.

In production:

- Separate cache busting filenames from `ManifestStaticFilesStorage` and rspack allow us to set far-future expiry headers on all static assets.
- I'm serving static assets from the same origin as the website itself. (rspack can be configured for different requirements!)
- I don't worry anymore about duplicating assets which are both referenced from frontend code and backend code. This doesn't affect many assets after all.
- The HTML snippet is loaded once only.

## Example configuration

rspack.config.js:

    :::javascript
    module.exports = (env, argv) => {
      const { base, devServer, assetRule, postcssRule, swcWithPreactRule } =
        require("./rspack.library.js")(argv.mode === "production")

      const cfg = {
        ...base,
        devServer: devServer({ backendPort: env.backend }),
        module: {
          rules: [
            assetRule(),
            postcssRule({
              plugins: [
                "postcss-nesting",
                "autoprefixer",
              ],
            }),
            swcWithPreactRule(),
          ],
        },
        experiments: { outputModule: true },
        externals: {
          "django-prose-editor/editor": "import django-prose-editor/editor",
          "django-prose-editor/configurable":
            "import django-prose-editor/configurable",
        },
      }
      console.debug(JSON.stringify(cfg))
    }


settings.py:

    WEBPACK_ASSETS = BASE_DIR / "static"

base.html:

    {% load webpack_assets %}
    {% if not TESTING %}{% webpack_assets 'main' %}{% endif %}


webpack_assets.py:

    from functools import cache

    from django import template
    from django.conf import settings
    from django.utils.html import mark_safe


    register = template.Library()


    def webpack_assets(entry):
        path = settings.BASE_DIR / ("tmp" if settings.DEBUG else "static") / f"{entry}.html"
        return mark_safe(path.read_text())


    if not settings.DEBUG:
        webpack_assets = cache(webpack_assets)
    register.simple_tag(webpack_assets)


## The library which enables the nice configuration above

Of course, the whole ugly library has to be somewhere. Here is the current
version at the time of writing:

rspack.library.js:

    :::javascript
    /*
    Somewhat reusable webpack configuration chunks

    A basic rspack file may looks as follows:

        module.exports = (env, argv) => {
          const {
            base,
            devServer,
            assetRule,
            postcssRule,
            swcWithPreactRule,
            resolvePreactAsReact,
          } = require("./rspack.library.js")(argv.mode === "production")

          return {
            ...base,
            ...resolvePreactAsReact(),
            devServer: devServer({ backendPort: env.backend }),
            module: {
              rules: [
                assetRule(),
                postcssRule({
                  plugins: [
                    [
                      "@csstools/postcss-global-data",
                      { files: ["./frontend/styles/custom-media.css"] },
                    ],
                    "postcss-custom-media",
                    "postcss-nesting",
                    "autoprefixer",
                  ],
                }),
                swcWithPreactRule(),
              ],
            },
          }
        }

    NOTE: PLEASE DO NOT EVER UPDATE THIS FILE WITHOUT CONTRIBUTING THE CHANGES BACK
    TO FH-FABLIB AT https://github.com/feinheit/fh-fablib

    */

    const path = require("node:path")
    const HtmlWebpackPlugin = require("html-webpack-plugin")
    const rspack = require("@rspack/core")
    const assert = require("node:assert/strict")
    const semver = require("semver")

    assert.ok(semver.satisfies(rspack.rspackVersion, ">=1.1.3"), "rspack outdated")

    const truthy = (...list) => list.filter((el) => !!el)

    module.exports = (PRODUCTION) => {
      const cwd = process.cwd()

      function swcWithPreactRule() {
        return {
          test: /\.(j|t)sx?$/,
          loader: "builtin:swc-loader",
          exclude: [/[\\/]node_modules[\\/]|foundation/],
          options: {
            jsc: {
              parser: {
                syntax: "ecmascript",
                jsx: true,
              },
              transform: {
                react: {
                  runtime: "automatic",
                  importSource: "preact",
                },
              },
              externalHelpers: true,
            },
          },
          type: "javascript/auto",
        }
      }

      function swcWithReactRule() {
        return {
          test: /\.(j|t)sx?$/,
          loader: "builtin:swc-loader",
          exclude: [/[\\/]node_modules[\\/]|foundation/],
          options: {
            jsc: {
              parser: {
                syntax: "ecmascript",
                jsx: true,
              },
              transform: {
                react: {
                  runtime: "automatic",
                  // importSource: "preact",
                },
              },
              externalHelpers: true,
            },
          },
          type: "javascript/auto",
        }
      }

      function htmlPlugin(name = "", config = {}) {
        return new HtmlWebpackPlugin({
          filename: name ? `${name}.html` : "[name].html",
          inject: false,
          templateContent: ({ htmlWebpackPlugin }) =>
            `${htmlWebpackPlugin.tags.headTags}`,
          ...config,
        })
      }

      function htmlSingleChunkPlugin(chunk = "") {
        return htmlPlugin(chunk, chunk ? { chunks: [chunk] } : {})
      }

      function postcssLoaders(plugins) {
        return [
          { loader: rspack.CssExtractRspackPlugin.loader },
          { loader: "css-loader" },
          { loader: "postcss-loader", options: { postcssOptions: { plugins } } },
        ]
      }

      function cssExtractPlugin() {
        return new rspack.CssExtractRspackPlugin({
          filename: PRODUCTION ? "[name].[contenthash].css" : "[name].css",
          chunkFilename: PRODUCTION ? "[name].[contenthash].css" : "[name].css",
        })
      }

      return {
        truthy,
        base: {
          // mode: PRODUCTION ? "production" : "development",
          // bail: PRODUCTION,
          context: path.join(cwd, "frontend"),
          entry: { main: "./main.js" },
          output: {
            clean: PRODUCTION,
            path: path.join(cwd, PRODUCTION ? "static" : "tmp"),
            publicPath: "/static/",
            filename: PRODUCTION ? "[name].[contenthash].js" : "[name].js",
            // Same as the default but prefixed with "_/[name]."
            assetModuleFilename: "_/[name].[hash][ext][query][fragment]",
          },
          plugins: truthy(cssExtractPlugin(), htmlSingleChunkPlugin()),
          target: "browserslist:defaults",
        },
        devServer(proxySettings) {
          return {
            host: "0.0.0.0",
            hot: true,
            port: Number(process.env.PORT || 4000),
            allowedHosts: "all",
            client: {
              overlay: {
                errors: true,
                warnings: false,
                runtimeErrors: true,
              },
            },
            devMiddleware: {
              headers: { "Access-Control-Allow-Origin": "*" },
              index: true,
              writeToDisk: (path) => /\.html$/.test(path),
            },
            proxy: [
              proxySettings
                ? {
                    context: () => true,
                    target: `http://127.0.0.1:${proxySettings.backendPort}`,
                  }
                : {},
            ],
          }
        },
        assetRule() {
          return {
            test: /\.(png|webp|woff2?|svg|eot|ttf|otf|gif|jpe?g|mp3|wav)$/i,
            type: "asset",
            parser: { dataUrlCondition: { maxSize: 512 /* bytes */ } },
          }
        },
        postcssRule(cfg) {
          return {
            test: /\.css$/i,
            type: "javascript/auto",
            use: postcssLoaders(cfg?.plugins),
          }
        },
        sassRule(options = {}) {
          let { cssLoaders } = options
          if (!cssLoaders) cssLoaders = postcssLoaders(["autoprefixer"])
          return {
            test: /\.scss$/i,
            use: [
              ...cssLoaders,
              {
                loader: "sass-loader",
                options: {
                  sassOptions: {
                    includePaths: [path.resolve(path.join(cwd, "node_modules"))],
                  },
                },
              },
            ],
            type: "javascript/auto",
          }
        },
        swcWithPreactRule,
        swcWithReactRule,
        resolvePreactAsReact() {
          return {
            resolve: {
              alias: {
                react: "preact/compat",
                "react-dom/test-utils": "preact/test-utils",
                "react-dom": "preact/compat", // Must be below test-utils
                "react/jsx-runtime": "preact/jsx-runtime",
              },
            },
          }
        },
        htmlPlugin,
        htmlSingleChunkPlugin,
        postcssLoaders,
        cssExtractPlugin,
      }
    }
