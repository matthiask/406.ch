Title: How I handle versioning
Categories: Django, Programming
Draft: remove-this-to-publish

I have been reading up on versioning methods a bit, and I noticed that I never
shared my a bit unorthodox versioning method. I previously wrote about my [rules for releasing open source software](https://406.ch/writing/my-rules-for-releasing-open-source-software/) but skipped everything related to versioning.

I use something close to the ideas of [semantic versioning](https://semver.org/) but it's not quite that. Note that the versioning scheme has nothing to do with production readiness, it's more about communicating the state of the project.


## 0.0.x -- Everything breaks

I don't trust my choices a lot. Everything may radically change, and I may also abandon the project with no hard feelings.

## 0.1.0 -- Changelogging

I generally start writing release notes or rather a [Changelog](https://en.wikipedia.org/wiki/Changelog), since writing full release notes is much more work. You absolutely have to test the software and I do not guarantee anything related to backwards compatibility -- just that you'll know about breaking changes when you read the CHANGELOG.

## ?.?.x -- Bugfixes and pure additions

Strictly speaking, patch version increments are only for bugfixes. However, when I add new features which are purely additional to the package or if there's no way (famous last words) that anything will break, I'll upload a patch release.

Sometimes it might be better to increment the minor version, yes. But, being very lazy, I sometimes only want to add a line to the CHANGELOG instead of adding a new heading for the new release. Also, if I don't quickly release new additions there's a real danger that I'll only come back to the project weeks or months later, and I don't want anyone (myself included) waiting on these updates. Also, if I inadvertently introduced new bugs it's better to fix them quickly instead of forgetting about it first and having to rediscover the buggy code later.


## 1.0.0 -- I'm happy

I'm happy with the package and I commit to start using semver more properly. If I have to (or want to) break backwards compatibility you get a migration path, especially if I need it myself. Which is often the case since I'm maintaining dozens of Django-based websites and webapps, and I'm always [dogfooding](https://en.wikipedia.org/wiki/Eating_your_own_dog_food) my stuff.

The pure additions case from the last section still applies, since slapping a 1.0 version on something doesn't suddenly make me less lazy.


## Outliers

[FeinCMS](https://github.com/feincms/feincms) uses a variant of [calendar versioning](https://calver.org/); the version at the time of writing is 24.8.2 which means the second release in August 2024.

There are probably other outliers I forgot about.
