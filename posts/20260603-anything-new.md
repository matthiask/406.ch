Title: Anything new?
Categories: Django, Programming

# Anything new?

A lot of time has passed since I officially announced that I want to [step down from maintaining django-mptt](https://406.ch/writing/weeknotes-2021-week-10/#django-mptt-is-not-maintained-anymore). I started contributing around 2009, tagged the [0.3 release in April 2010](https://github.com/django-mptt/django-mptt/tree/0.3.0), and have been the sole active maintainer since somewhere around 2019. The post about [django-tree-queries](https://406.ch/writing/django-tree-queries/) has more background, but that's not today's topic.


## Stepping away isn't easy

For me, abandoning a project is a bit like stepping out of a relationship: negative emotions end up being a somewhat necessary driver, because the absence of positive events alone rarely provides enough force on its own. I get a lot of satisfaction from a job well done, and walking away means letting that go.

Even with time set aside for open source in my work day, I still have to choose where that time goes. django-mptt stopped being where it needed to go.


## The sense of entitlement

When a project is obviously unmaintained, asking for free labor is walking a tightrope. It takes real care not to rekindle exactly the frustrations that led maintainers away in the first place.

It takes energy not to clap back when someone is being rude or insensitive in the issue tracker. Asking "Anything new?" on a ticket where the next steps were outlined clearly and obviously nothing happened in the meantime is just one variant of this.

Quietly quitting isn't what I want to do — and as a user of django-mptt myself, I can't really do that either. Taking the high road is the professional choice. But it costs something.

I keep coming back to [Mona Eltahawy on refusing to be civil](https://youtu.be/Amj3QG2s1BI?t=226). She's speaking about something quite different, and I'm aware I write this as a white man. The situations aren't the same at all. But she articulated something I haven't managed to put into words as well myself and I like the idea of speaking up and taking the fight to those who awaken these feelings instead of taking the high road.


## Doing it with AI

No post these days is complete without the obligatory AI mention, but there's some relevancy to it.

I fixed and closed almost all open django-mptt issues in a two-hour Claude session. I've previously written about using [LLMs for open source maintenance](https://406.ch/writing/llms-for-open-source-maintenance-a-cautious-case/), and the productivity gain is real whatever the detractors say. And the quality isn't suddenly getting worse. Code wasn't perfect before either. The test suite allows a certain degree of trust in the result and according to [my rules for releasing Open Source software](https://406.ch/writing/my-rules-for-releasing-open-source-software/) we don't have to require more than that.

It doesn't change the underlying dynamic, though. [rsync and outrage](https://medium.com/@tridge60/rsync-and-outrage-d9849599e5a0) illustrates the trap neatly: Tridgell got flooded with AI-generated security reports, used AI to handle them, and then got criticized for using AI. The tools that created the workload aren't allowed to address it. The expectation is that the work has to involve sweat and tears and uncountable unpaid hours.

The common goal should be more and better open source software. What we get as Open Source maintainers is shit from both sides: One side took our free work and trained models on it without asking, the other side complains about the supposedly unethical use of AI while acting in unethical ways themselves.

There's something Kantian about how open source contribution gets framed. [Kant](https://en.wikipedia.org/wiki/Immanuel_Kant)'s argument was that the only truly moral acts are those driven by duty and good will — not by desire, inclination, or any expectation of compensation. By that logic, I'm only acting morally if I keep going despite the burnout and the entitlement. If I stop, I'm not.

It's bleak. The problems with AI are real. The people controlling the large models are assholes. But I have to work in the world as it is while also trying to change it for the better.
