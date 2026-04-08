Title: Switching all of my Python packages to PyPI trusted publishing
Categories: Django, Programming
Draft: remove-this-to-publish

As I have teased on [Mastodon](https://hachyderm.io/@matthiask/116300209761371116), I'm switching all of my packages to PyPI trusted publishing. I have been using it to release the [django-debug-toolbar](github.com/django-commons/django-debug-toolbar) a few times but never set it up myself. The process seemed tedious.

The malicious releases uploaded to PyPI two weeks ago and the blog post about [digital attestations in `pylock.toml`](https://snarky.ca/why-pylock-toml-includes-digital-attestations/) finally pushed me to make the switch. All of my PyPI tokens have been revoked so there is no quick shortcut.

!!! Note
    I'm also looking at other code hosting platforms. I have been using git before GitHub existed and I'll probably still use git when GitHub has completed its enshittification. For now the cost/benefit ratio of staying on GitHub is still positive for me. Trusted publishing isn't available everywhere, so for now it is GitHub anyway.

In the end, switching an existing project was easier than expected. I have completed the process for [django-prose-editor](https://github.com/feincms/django-prose-editor) and [feincms3-cookiecontrol](https://github.com/feincms/feincms3-cookiecontrol/).

For my future benefit, here are the step by step instructions I have to follow:

0. Have a package which is buildable using e.g. `uvx build`

1. On PyPI add a trusted publisher in the project's publishing settings:
    - Owner: `matthiask`, `feincms`, `feinheit`, whatever the user or organization's name is.
    - Repository: `django-prose-editor`
    - Workflow name: `publish.yml`
    - Environment: `release`

2. In the GitHub repository, create a `release` environment in Settings / Environments. Add myself and potentially also other releasers as a required reviewer. I allow self-review and disallow administrators to bypass the protection rules.

3. Run `git tag x.y.z` and `git push`, no more `uvx twine` or `hatch publish`.

4. Approve the release in the actions tab on the repository.

5. Either enjoy or swear and repeat the steps.

I'm happy with testing the release process in production. The older I get the less I care if people think I'm stupid. That's also why feincms3-cookiecontrol 1.7.0 doesn't exist, only 1.7.1 -- the process failed and I had to bump the patch version and try again. Copy the `publish.yml` from a known good place, for example from the [django-prose-editor repository](https://github.com/feincms/django-prose-editor/blob/main/.github/workflows/publish.yml). I have added the `if: github.repository == 'feincms/django-prose-editor'` statement which ensures that the workflow only runs in the main repository, but that's optional if you don't care about failing workflows.
