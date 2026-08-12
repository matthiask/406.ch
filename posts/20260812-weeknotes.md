Title: Weeknotes (2026 week 33)
Categories: Climate, Django, Programming, Weeknotes
Draft: remove-this-to-publish

## Holidays and the heat wave

I had four weeks of holidays this summer. The timing couldn't have been much better with the heat wave -- doing much thinking seems to be impossible anyway. I organized a multi-day feast with a few friends and with much help from others. We built up the site and installations over the course of multiple days and spent some days tearing most of it down afterwards. I started back to the office job physically tired but mentally rested. That's good. I'm really looking forward to seeing the pictures people took.

What's less good is that we're living through the [projections](https://www.ipcc.ch/report/ar1/wg1/) which climate scientists warned us about decades ago. Or worse, even, since Switzerland is one of the regions where the temperature increased more than the global average. The member of Switzerland's [Federal Council](https://www.admin.ch/en/the-federal-council) heading the Federal Department of the Environment, Transport, Energy and Communications reportedly said that he didn't [expect such intense heat](https://www.tagesanzeiger.ch/albert-roesti-diese-hitze-haette-ich-nicht-erwartet-276779425825). Of course, it was reported earlier in the same week that the same member was responsible for [removing funding for a more resilient forest](https://www.srf.ch/news/schweiz/hitzeresistente-baeume-bundesrat-roesti-streicht-mittel-fuer-klimatauglichen-wald) from the budget for the next fiscal year. This is unfortunately to be expected: he has long been connected to the fossil energy industry. After all, he was also the president of [Swissoil](https://www.watson.ch/schweiz/klima/206672787-albert-roesti-laesst-swissoil-mandat-von-webseite-verschwinden) and [Auto Schweiz](https://de.wikipedia.org/wiki/Albert_R%C3%B6sti). It's really frustrating. None of this is news to climate scientists, and it hasn't been news [here](/writing/category-climate/) either -- these posts start in 2005, back when I was studying environmental sciences at ETH with a focus on atmospheric physics.


## Scripts for auto-merging dependabot and pre-commit pull requests

I let Claude write some scripts for automatically merging pull requests created by various bots, [see here](https://github.com/feincms/.github). The script finds pull requests created by a predefined list of bots in a defined list of accounts (organizations or users) and squash-merges them if the CI run is green and there are no conflicts. It's a dry run by default; `--apply` is required to actually merge anything. It doesn't look at reviews and doesn't care whether a bump is major or minor -- I'm relying on the test suites for that.

The [ruff 0.16](https://astral.sh/blog/ruff-v0.16.0) update was a bit painful because ruff now enables 413 rules by default, up from 59. Recurring themes were warnings about mutable class variables (which are common when using Django), blind `except` clauses and underspecified dates without time zones, but none of them in scenarios where they actually hurt.

So, instead of just running the merge script, I had to fix up dozens of `pyproject.toml` files and projects. Oh well, next time will be smooth again.


## Releases

Since I've been away from the computer for so long, the list of releases from the start of July onwards is quite short.

### django-authlib

[django-authlib 0.18](https://pypi.org/project/django-authlib/) now also supports Microsoft Entra ID logins. The admin integration also has support for Microsoft accounts, not just for Google.

### django-content-editor

The [django-content-editor 9.0.1](https://pypi.org/project/django-content-editor/) just contains a small fix which avoids submitting the form that allows cloning content between regions when cancelling the dialog.
