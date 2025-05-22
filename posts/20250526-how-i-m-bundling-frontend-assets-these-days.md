Title: How I'm bundling frontend assets using Django and rspack these days
Categories: Django, Programming

I last wrote about configuring Django with bundlers in 2018: [Our approach to configuring Django, Webpack and ManifestStaticFilesStorage](https://406.ch/writing/our-approach-to-configuring-django-webpack-and-manifeststaticfilesstorage/). An update has been a long time coming. I wanted to write this down for a while already, but each time I started explaining how configuring rspack is actually nice I look at the files we're using and switch to writing about something else. This time I managed to get through -- it's not that bad, I promise.

This is quite a long post. A project where all of this can be seen in action is [Traduire](https://github.com/matthiask/traduire/), a platform for translating gettext catalogs. I announced it on the [Django forum](https://forum.djangoproject.com/t/traduire-a-platform-for-editing-gettext-translations-on-the-web/32687).

## Our requirements

The requirements were still basically the same:

- Hot module reloading during development
- A process which produces hashed filenames depending on their content so that
  we can use far-future expiry headers to cache assets in browsers
- While running Node.js in development is fine we do not want Node.js on the
  server (in the general case)
- We still want transpiling and bundling for now

We have old projects using SASS. These days we're only using PostCSS
(especially [autoprefixer](https://github.com/postcss/autoprefixer) and maybe
[postcss-nesting](https://github.com/csstools/postcss-plugins/tree/main/plugins/postcss-nesting).
Rewriting everything is out of the question, so we needed a tool which handled
all that as well.

People in the frontend space seem to like tools like Vite or Next.js a lot. I
have also looked at Parcel, esbuild, rsbuild and others. Either they didn't
support our old projects, were too limited in scope (e.g. no HMR), too
opinionated or I hit bugs or had questions about their maintenance. I'm sure
all of them are great for some people, and I don't intend to talk badly about
any of them!

In the end, the flexibility, speed and trustworthiness of
[rspack](https://rspack.dev/) won me over even though I have a love-hate
relationship with the Webpack/rspack configuration. We already had a reusable
library of configuration snippets for webpack though and moving that library
over to rspack was straightforward.

That being said, configuring rspack from scratch is no joke, that's why tools
such as [rsbuild](https://rsbuild.dev/) exist. If you already know Webpack well
or really need the flexibility, going low level can be good.


## High-level project structure

The high-level overview is:

- Frontend assets live in their own folder, `frontend/`.
- We're using [fabric](https://www.fabfile.org/) and
  [rspack](https://rspack.dev/), their configuration resides in the root folder
  of the project as does Django's `manage.py`.
- The frontend is transpiled and bundled directly into `static/` for production and into `tmp/` during development.
- We use the HTML plugin of rspack to emit snippets containing `<link>` and `<script>` tags. The HTML snippet can be included as-is, without any postprocessing.
- `frontend/` or `frontend/static` is optionally added to `STATICFILES_DIRS` so that some of the files from the frontend can easily be referenced in `{% static %}` tags.

During development:

- We use the dev server of rspack/node to handle `127.0.0.1:8000`. This server handles requests for frontend assets and the websocket for hot module reloading and proxies everything else to the Django backend running on a different random port.

During deployment:

- The assets are compiled to `static/` and either rsynced to the server or added to the container separately from the standard `./manage.py collectstatic --noinput`.

In production:

- Separate cache busting filenames from `ManifestStaticFilesStorage` and rspack allow us to set far-future expiry headers on all static assets.
- I'm serving static assets from the same origin as the website itself. (rspack can be configured for different requirements!)
- I don't worry anymore about duplicating assets which are both referenced from frontend code and backend code. This doesn't affect many assets after all.
- The HTML snippet is loaded once only.

## Example configuration

Here's an example configuration which works well for us. What follows is the
rspack configuration itself, building on our snippet library
`rspack.library.js`. We mostly do not change anything in here except for the
list of PostCSS plugins:

rspack.config.js:

    :::javascript
    module.exports = (env, argv) => {
      const { base, devServer, assetRule, postcssRule, swcWithPreactRule } =
        require("./rspack.library.js")(argv.mode === "production")

      return {
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
      }
    }

The default entry point is `main` and loads `frontend/main.js`. The rest of the
JavaScript and styles are loaded from there.

The HTML snippet loader works by adding `WEBPACK_ASSETS = BASE_DIR / "static"` to the Django settings and adding the following tags to the `<head>` of the website, most often in `base.html`:

    :::html+django
    {% load webpack_assets %}
    {% webpack_assets 'main' %}

The corresponding template tag in `webpack_assets.py` follows:

    :::python
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


Last but not least, the fabfile contains the following task definition:

    :::python
    @task
    def dev(ctx, host="127.0.0.1", port=8000):
        backend = random.randint(50000, 60000)
        jobs = [
            f".venv/bin/python manage.py runserver {backend}",
            f"HOST={host} PORT={port} yarn run rspack serve --mode=development --env backend={backend}",
        ]
        # Run these two jobs at the same time:
        _concurrently(ctx, jobs)

The fh-fablib repository contains the [`_concurrently`](https://github.com/feinheit/fh-fablib/blob/8109a76b63b37d3433356fabb4469263f8b18d66/fh_fablib/__init__.py#L194-L214) implementation we're using at this time.


## The library which enables the nice configuration above

Of course, the whole library of snippets has to be somewhere. The fabfile automatically updates the library when we release a new version, and the library is the same in all the dozens of projects we're working on. Here's the current version of `rspack.library.js`:

    :::javascript
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
          exclude: [/node_modules/],
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
          exclude: [/node_modules/],
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

## Closing thoughts

Several utilities from this library aren't used in the example above, for
example the `sassRule` or the HTML plugin utilities which are useful when you
require several entry points on your website, e.g. an entry point for the
public facing website and an entry point for a dashboard used by members of the
staff.

Most of the code in here is freely available in our
[fh-fablib](https://github.com/feinheit/fh-fablib) repo under an open source
license. Anything in this blog post can also be used under the
[CC0](https://creativecommons.org/public-domain/cc0/) license, so feel free to
steal everything. If you do, I'd be happy to hear your thoughts about this
post, and please share your experiences and suggestions for improvement -- if
you have any!
