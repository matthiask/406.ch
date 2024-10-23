Title: Weeknotes (2024 week 43)
Categories: Django, Programming, Weeknotes


I had some much needed time off, so this post isn't that long even though [four weeks have passed since the last entry](https://406.ch/writing/weeknotes-2024-week-39/).


## From webpack to rspack

I've been really happy with [rspack](https://rspack.dev/) lately. Converting
webpack projects to rspack is straightforward since it mostly supports the same
configuration, but it's much much faster since it's written in Rust. Rewriting
things in Rust is a recurring theme, but in this case it really helps a lot.
Building the frontend of a larger project of ours consisting of several admin
tools and complete frontend implementations for different teaching materials
only takes 10 seconds now instead of several minutes. That's a big and relevant
difference.

Newcomers should probably still either use [rsbuild](https://rsbuild.dev/),
[Vite](https://vite.dev/) or maybe no bundler at all. Vanilla JS and browser
support for ES modules is great. That being said, I like cache busting,
optimized bundling and far-future expiry headers in production and hot module
reloading in development a lot, so learning to work with a frontend bundler is
definitely still worth it.


## Dark mode and light mode

I have been switching themes in my preferred a few times per year in the past. The following ugly bit of vimscript helps switch me the theme each time the sun comes out when working outside:

    let t:light = 0
    function! FiatLux()
        if t:light == 0
            :set background=light
            let t:light = 1
        else
            :set background=dark
            let t:light = 0
        endif
    endfunction
    nnoremap <F12> :call FiatLux()<CR>

I'm using the [Ptyxis](https://devsuite.app/ptyxis/) terminal emulator
currently, I haven't investigated yet if there's a way to toggle dark and light
mode for it as well. Using F10 to open the main menu works fine though, and
using the mouse wouldn't be painful either.


## Helping out in the Django forum and the Discord

I have found some pleasure in helping out in the [Django
Forum](https://forum.djangoproject.com/) and in the official [Django
Discord](https://discord.gg/xcRH6mN4fa). I sometimes wonder why more people
aren't reading the Django source code when they hit something which looks like
a bug or something which they do not understand. I find Django's source code
very readable and I have found many nuggets within it. I'd always recommend
checking the documentation or maybe official help channels first, but the code
is also out there and that fact should be taken advantage of.


## Releases

- [django-content-editor 7.1](https://pypi.org/project/django-content-editor/):
  Fixed a bug where the ordering and region fields were handled incorrectly
  when they appear on one line in the fieldset. Also improved the presentation
  of inlines in unknown regions and clarified the meaning of the move to region
  dropdown. Also, released the improvements from previous patch releases as a
  new minor release because that's what I should have been doing all along.
- [form-designer 0.27](https://pypi.org/project/form-designer/): A user has
  been bitten by ``slugify`` removing cyrillic characters because it only keeps
  ASCII characters around. Here's the wontfixed bug in the Django issue
  tracker: [#8391](https://code.djangoproject.com/ticket/8391). I fixed the
  issue by removing the slugification (is that even a word?) when generating
  choices.
