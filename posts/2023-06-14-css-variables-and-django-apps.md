Title: CSS variables and immutability
Date: 2023-06-14
Categories: Django, Programming, feincms

# Using CSS variables[^variables] to ship customizable CSS in Django apps

[^variables]: Custom properties would probably be the more correct naming, but CSS variables is nicer to say.

I have been working with [SASS](https://sass-lang.com/) for a long time but
have been moving towards writing CSS with a few [PostCSS](https://postcss.org/)
goodies in the last years. At first, I just replaced the `$...` with
`var(--...)` and didn't think much about it. The realization that CSS variables
can be more than that came later. Edit basic values directly in the browser and
immediately see the results! Change CSS depending on media queries or the
cascade!

With all that power came back the wish to not just ship backend and HTML code
in Django apps I (help) maintain but also reusable CSS, with a few overrideable
CSS variables for basic changes to the visual style. Loading `.scss` files from
somewhere inside `venv/lib/python3.11/site-packages/<package>/styles/` would of
course have been possible, but very obscure. Also, not everyone puts their
virtualenv at `venv`, the `README` instructions for those packages would
quickly have become unwieldy. CSS variables paved the way for shipping CSS as a
Django static file while still allowing customizability by leveraging the
functionality of the browser itself instead of the frontend build toolchain.

## Patterns for overrideable values

A pattern for defining defaults for CSS variables is to always define the
fallback (the example is intentionally bad but inspired by real world
experiences when developing
[feincms3-cookiecontrol](https://github.com/feinheit/feincms3-cookiecontrol)):

    :::css
    .box {
      background: var(--box-background, #222);
      color: var(--box-foreground, #fff);
    }

## Less repetition (but trouble awaits)

If `--box-background` isn't set the `var()` function falls back to the second
argument, `#222`. Repeating this value over and over gets annoying quickly, so
you define a few defaults on the `:root` element and use those variables in the
code, without specifying the default again:

    :::css
    :root {
      --box-background: #222;
      --box-foreground: #fff;
    }

    .box {
      background: var(--box-background);
      color: var(--box-foreground);
    }

The project can now override the default background color using:

    :::css
    :root {
      --box-background: #444;
      --box-foreground: #ccc;
    }

Of course now you're back at the mercy of CSS loading order. If the app's CSS
is loaded first, everything works. If not, your custom value is immediately
overwritten. You could avoid this by overwriting the default lower in the cascade:

    :::css
    .box {
      --box-background: #444;
      --box-foreground: #ccc;
    }

Great, everything works again!

Later, the box also contains a button which uses a different background but the
same foreground, so of course we add more variables in the package:

    :::css
    :root {
      --box-background: #222;
      --box-foreground: #fff;
      --box-button-background: #333;
      --box-button-foreground: var(--box-foreground);
    }

What happens now when overwriting the `--box-foreground` variable just for the
`.box` element?

You're not sure? I certainly wasn't and am not. But what I remember happening
was that the overridden foreground color was just applied to the text and not
to the button itself. I was confused (it seems clearer in hindsight...)

## A better way

If values are supposed to be overridden and only used inside components, a
better way is to define local CSS for components by following a convention
(underscore prefix for local/private variables):

    :::css
    /* Defined on .box, not :root */
    .box {
      --_background: var(--box-background, #222);
      --_foreground: var(--box-foreground, #fff);
      --_button-background: var(--box-button-background, #333);
      --_button-foreground: var(--box-button-foreground, var(--_foreground));
    }

And then you only use the prefixed versions inside the component:

    :::css
    .box {
      background: var(--_background);
      color: var(--_foreground);
    }

    .box__button {
      background: var(--_button-background);
      color: var(--_button-foreground);
    }

The `--box-*` variables are undefined by default; the only time when they are
set is when the user of the package wants to override those values. If you only
overide the box foreground the button also inherits the new foreground color.
And while there would certainly be a way to achieve the same thing with the old
way above it's certainly not as simple to explain.

The reason why it's simple to explain is **immutability**. The CSS variables
which are overrideable by the user are only ever read by the package, never
written to.
