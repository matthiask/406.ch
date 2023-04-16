Title: Using Bliss with webpack
Slug: using-bliss-with-webpack
Date: 2018-04-30
Categories: Programming
Type: markdown

# Using Bliss with webpack

I really like [bliss](https://blissfuljs.com/). It makes writing JavaScript much more fun, and JavaScript awesomely lightweight.

Also, I learnt a lot while reading the code and the documentation.

However, since Bliss wants to inject itself into the global namespace and isn't designed to be consumed as a NPM module I had some trouble finding a good way to use it with [webpack](https://webpack.js.org/). I finally found a good way to combine the two; short instructions follow:

Install the newest and best version of bliss:

    yarn add https://github.com/LeaVerou/bliss/

Import Bliss near the top into your main JavaScript file (the file which is your webpack entrypoint). Since we're using a source checkout, there is no combined `bliss.js` file. Let's import the two parts of `bliss.js` directly instead:

    import 'blissfuljs/bliss.shy.js'
    import 'blissfuljs/bliss._.js'

(I'm fine with Bliss taking the `window.$` and `window.$$` (resp. `s/window/self/`) variables, and with Bliss being available outside the webpack build.)

In all files where you want to use write blissful JavaScript, add the following line so that [ESLint](https://eslint.org/) does not complain:

    const {$, $$} = window  // eslint-disable-line

The `eslint-disable-line` avoids unused variable warnings. I wouldn't recommend disabling ESLint (or other code linters) too much, but in this case, it's fine.

Also, you should check out the [CSS Secrets by Lea Verou](https://www.amazon.com/CSS-Secrets-Lea-Verou/dp/1449372635?tag=leaverou-20) book if you do not know it already.
