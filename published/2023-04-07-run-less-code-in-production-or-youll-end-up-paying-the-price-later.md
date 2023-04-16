Title: Run less code in production or you’ll end up paying the price later
Slug: run-less-code-in-production-or-youll-end-up-paying-the-price-later
Date: 2023-04-07
Categories: Django, Programming
Type: markdown

# Run less code in production or you'll end up paying the price later

At [work](https://feinheit.ch/) we do have the problem of dependencies which aren't maintained anymore. That's actually a great problem to have because it means that the app or website ended up running for a long time, maybe longer than expected initially. I think that websites have a lifetime of 3-5 years[^lifetime] which is already much longer than the lifetime of major versions of some rapid development frameworks, especially frontend frameworks. We have been using [Zurb Foundation](https://get.foundation/) in the past. It has served us well and I don't want to dunk on it – after all it is free, it has great documentation and it works well. It has many features and many components, but as changes happen, not just in the framework itself but also in the tooling it uses upgrades stay hard and things start to break somewhere down the road (for example when [Dart Sass 2.0 will be released](https://github.com/sass/dart-sass). And when that happens you have to pick up the parts and maintain them yourself -- having grown your codebase by a considerable amount practically overnight.

Of course it's also hard to argue for starting to write all HTML, CSS and JavaScript from scratch. [Standards are very helpful.](https://406.ch/writing/flake8-and-value-standards/) Building without some sort of standardized tooling will not only lead to rank growth but also means that you have to make many many small and (relatively) irrelevant decisions _and you have to justify those decisions when working in a team_ because you could just as well have decided differently.

So after all that, should you use frontend frameworks? The answer is -- as always -- it depends.

You should definitely use a framework when prototyping.

But already when working on a MVP it gets less and less clear. You're kidding yourself if you think that sometime in the future you'll have the time to clean up your code base; **of course** you're always refactoring and **of course** you'll try to always leave each part behind a little bit nicer than it was before, but even then the big rewrite didn't happen and you'll continue using at least some aspects of the code that was hastily written for the initial release.

The exceptions to the rule are frameworks and tools which have a proven track record of maintaining stability over time. So, despite the fact that [the Django framework](https://www.djangoproject.com/) has more than 100'000 lines of code I feel good about using it. Django was released as Open Source in July 2005 and has been steadily maintained over the last nearly 18 years. [Funding](https://www.djangoproject.com/fundraising/) is always a problem (contribute if you can!) but at least the Django software foundation manages to employ two Django fellows which are certainly key in driving the framework forward.

Again the picture gets less clear when third party apps are involved. Some third party apps were actively maintained several years ago and now they aren't. I have personally taken over the maintenance of several such apps or more often than not reimplemented them with less functionality and much less code. Sometimes it's easier to maintain a little more of your own code instead of much more of someone else's code.

So, what's the take away?

Maybe pay attention to the following points:

- Recent activity on the repository, recent releases and good docs are always a good sign for the health of a project.
- Take the time to read at least a part of the code of third party projects before starting to rely on them. It's a bad idea to just read the documentation and nothing else. When it comes to Django apps I always at least read the model files to understand how the data's modeled and skim the views and forms.
- Have a look at issues and pull/merge requests. Don't worry about usage questions etc but mainly about "hard problem" issues.
- Try to stay away from packages which are too comprehensive; reusing these packages is hard even for their authors and when they are abandoned the amount of responsibility transferred to you will be so much bigger.

[^lifetime]: Citation required obviously, don't take my word on it. Data is certainly more long lived, but I have my doubts regarding the code running many small sites.
