Title: Unlearning SCSS to use CSS variables effectively
Date: 2023-05-31
Categories: Programming

# Unlearning SCSS to use CSS variables effectively

SCSS variables are a way to stop repeating the same values over and over. They
are very useful already, especially when used together with some of the more
interesting SCSS functions such as `brighten()`, `darken()` etc. CSS doesn't
really have ways to do the same yet. `hsl(var(...)...)` only gets you so far.

CSS variables are another beast. You can use them the same way by replacing `$`
with `--` but if you do this you're missing out big time on the features which
actually make CSS variables great: The cascade and the ability to update them
in response to media queries, interactions or other events.

The way I'm using CSS variables is:

- Define good defaults on the `:root` selector.
- Change those defaults in response to media queries, e.g. for large screens
  when writing mobile first CSS -- as you should.
- Override defaults in some contexts, e.g. in an `<aside>` or some other
  fitting component.

Suppose you wanted different spacings between components depending on the
breakpoint. You could go the fully fluid route with `clamp()`, `max()`, `min()`
and viewport-relative units. It's simpler to keep the complexity lower and use
breakpoints, certainly for me.

    :::css
    :root {
      --space: 1rem;
    }

    @media (min-width: 800px) {
      :root {
        --space: 2rem;
      }
    }

Now you can use `var(--space)` everywhere:

    :::css
    .box {
      margin-bottom: var(--space);
    }

The equivalent SCSS would probably look something like this, with a fitting
`breakpoint()` mixin:

    :::scss
    $space-sm: 1rem;
    $space-md: 2rem;

    .box {
      margin-bottom: $space-sm;

      @include breakpoint(md) {
        margin-bottom: $space-md;
      }
    }

That doesn't look too bad until you have to repeat the breakpoint in all your
components. That's when SCSS gets boring while CSS is staying awesome.

## Upping your game.

You could also use
[postcss-nesting](https://www.npmjs.com/package/@csstools/postcss-nesting-experimental)
and [postcss-custom-media](https://www.npmjs.com/package/postcss-custom-media)
and write:

    :::css
    @custom-media --media-md (min-width: 800px);

    :root {
      --space: 1rem;

      @media (--media-md) {
        --space: 2rem;
      }
    }

Nesting is definitely a two-edged sword though. CSS methodologies such as BEM
(Block Element Modifier) should generally fix the need to use nesting at all.
Nesting leads to overspecific CSS, and also to an enormous amount of generated
CSS which is also brittle and basically impossible to refactor ("write-only
CSS"). But, in some contexts it's really nice. I do like the fact that
indentation has a specific meaning if used like that.
