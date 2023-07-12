Title: How ruff changed my Python programming habits
Date: 2023-07-12
Categories: Django, Python, Programming

# How ruff changed my Python programming habits

[ruff](https://beta.ruff.rs/) isn't just a faster replacement for flake8, isort
and friends.

With other Python-based formatters and linters there's always a trade off
between development speed (waiting on `git commit` is very boring) and
strictness.

ruff is so fast that enabling additional rules is practically free in terms of
speed; the only question is if those rules lead to better, or maybe just to
more correct and consistent code.

I have long been using [pre-commit](https://pre-commit.com/), and even longer
flake8, black, isort. I have written a piece about [flake8 and the value of
standards](https://406.ch/writing/flake8-and-value-standards/) almost 9 years
ago and have continued moving in the mentioned direction ever since.

These days I have enabled a wide variety of rules. I'm not sold on all of them
(looking at you, pylint) and I'm definitely not of the opinion that rules which
I'm not using currently are worthless.

## Rules

### pyflakes, pycodestyle

No justification necessary, really.

### mccabe

I like the cyclomatic complexity checker, but I have relaxed it a bit. I find it very useful to avoid complex code, but some code is totally straightforward (e.g. building a queryset from a wide variety of query parameters) but still has many `if` statements. I'd rather allow more complexity instead of sprinkling the code with `# noqa` statements.

### isort

Sorted imports are great.

### pep8-naming

Mostly great except when it flags Django's migration files. The filenames
always start with numbers and that's obviously not a valid Python module name,
but it's not supposed to be.

### pyupgrade

pyupgrade is totally awesome.

### flake-2020

### flake8-boolean-trap

Sometimes annoying, mostly useful. I don't like that the plugin flags e.g. `with_tree_fields(True)` or `with_tree_fields(False)` because I don't think this could be possibly misread. But, apart from these edge cases it really is a good idea, especially since keyword-only arguments exist.

### flake8-bugbear

Mostly useful. I have disabled some of the more opinionated warnings though.

### flake8-comprehensions

### flake8-django

I actually like consistency. I also like flagging `fields = "__all__"`, but this check shouldn't trigger in admin `ModelForm` classes, really. I probably have to add another entry to `[tool.ruff.per-file-ignores]` for this.

### flake8-logging-format

I have removed this rule, I don't find it helpful.

### flake8-pie

### flake8-simplify

### flake8-gettext

Enormously useful and important. I don't know how many times I have encountered broken code like `gettext("Hello {name}".format(name=name))` instead of `gettext("Hello {name}").format(name=name)`.

### pygrep-hooks

### pylint

### RUF100

Ruff is able to automatically remove `# noqa` statements which don't actually silence any warnings. That's a great feature to have.

## Line length

Yes, let's go there. I still don't use longer lines than +/- 80 characters, but
I have disabled all line length warnings these days. I don't want to be warned
because I didn't break a string across lines.
