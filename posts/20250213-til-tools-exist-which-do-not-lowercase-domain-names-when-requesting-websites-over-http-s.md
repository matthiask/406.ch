Title: TIL: Tools exist which do not lowercase domain names when requesting websites over HTTP(S)
Categories: Programming, Django, TIL

About a week ago I received error mails for a surprising behavior (to me!)
where some tool requested an URL from one of our websites using
[feincms3-language-sites](https://github.com/feincms/feincms3-language-sites/)
(a Django library for multilingual websites) with a domain name containing
uppercase characters.

I knew that the domain part of all sorts of URLs is case sensitive, but what
surprised me was that our server actually got a request with such a domain
name, I hadn't really seen that before.

After researching a bit I learned that for example [curl](https://curl.se/)
intentionally preserves the casing of domain names, but browsers generally do
lowercase domains because it's more consistent. It's interesting that the
initial error was caused by a client with a proper Safari/macOS user agent, but
further research showed that the request was probably sent by something called
`go-social-activity-parser`, whatever that is.

I fixed the bug in
[feincms3-language-sites](https://github.com/feincms/feincms3-language-sites/)
and also in [feincms3-sites](https://github.com/feincms/feincms3-sites/) by
switching to case-insensitive matching of domain names. I have not yet added
punycode or IDNA equivalence to the code because I haven't needed it yet and
because I'm not 100% sure how to do it without breaking anything. Even though I
often work on websites in languages with lots of accents and umlauts we don't
use such domain names too often, so it hasn't been a problem yet. I'll cross
that bridge when I get there.
