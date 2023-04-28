Title: Weeknotes (2023 week 17)
Date: 2023-04-28
Categories: Politik, Django, Programming, Weeknotes

## Birthday

Another year achieved. Feels the same as last year. I'm glad.

## feincms3-cookiecontrol

I have released [feincms3-cookiecontrol
1.3](https://pypi.org/project/feincms3-cookiecontrol/). Mostly cleanups since
1.2, but also a new translation (already announced here). The script size has
been reduced from 4519 bytes to 4228 bytes (-6.5%) while keeping all features
intact. The reduction is totally meaningless but it was fun to do.

## oEmbed

I have been digging into the oEmbed spec a bit. I didn't even know that a
central list of [providers](https://oembed.com/providers.json) exists.
[Noembed](https://noembed.com/) still works great to embed many different types
of content but I worry more and more about its maintenance state.
Reimplementing the interesting parts shouldn't be that hard, but maybe I don't
have to do this myself. [oEmbedPy](https://github.com/attakei-lab/oEmbedPy/)
looks nice, I hope I get a chance to play around with it.
