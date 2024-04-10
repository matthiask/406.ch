Title: Building forms with the Django admin
Date: 2024-04-10
Categories: Django, Programming
Draft: remove-this-to-publish

# Building forms with the Django admin

The title of this post was shamelessly copied from [Jeff Triplett's post on
Mastodon](https://mastodon.social/@webology/112235938469045649).

## Why?

Many websites need a simple way of embedding forms, for example as a contact
form or for simple surveys to collect some data or inputs from visitors.
[Django's forms library](https://docs.djangoproject.com/en/5.0/topics/forms/)
makes building such forms straightforward but changing those forms requires
programming skills and programmer time. Both of them may not be readily
available. More importantly, sometimes it's just nice to give more tools to web
publishers.

The simple way to build something like this is to use a form builder such as
Google Forms, Typeform, Paperform or anything of the sort. Those options work
nicely. The downsides are that embedded forms using those services load slowly,
look differently, cost a lot or collect a lot of data on users, or all of those
options. Because of that there's still a place for building such functionality
locally.

If I wanted to use PHP and WordPress I could just use
[WPForms](https://wpforms.com/) and call it a day. Since I do not actually want
that this blog post is a bit longer.

## The early days: form-designer

One of the first Django-based third party apps I published was the [form-designer](https://github.com/feincms/form-designer). The first version was uploaded to PyPI in 2012 but it had already been used in production for more than two years at that point in time. I had used [Git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) for the deployment back then, before switching to [Python virtualenvs](https://virtualenv.pypa.io/) some time later (and never looking back!)

The form-designer is still maintained actively. Because of Django's stability and because of the fact that the app doesn't do all that much it doesn't require much development at all.

![A screenshot of the admin interface](https://406.ch/assets/20240410-form-designer.png)

The form designer supports a selection of standard HTML5 input fields out of the box and also has an optional [django-recaptcha](https://github.com/django-recaptcha/django-recaptcha) integration. All fields support some basic configuration such as setting a title, a help text, marking the field as required etc. Submissions can be sent to a configurable email address and can be saved in the database and later exported as an XLSX file. It's also possible to define your own actions.

## More flexibility needed: feincms3-forms

A few years back I mentioned [feincms3-forms in a weeknotes entry](https://406.ch/writing/weeknotes-2021-week-13-and-14/). The reasons why form-designer wasn't sufficient for a project back then are outlined in the blog post:

> ### feincms3-forms – A new forms builder for the Django admin interface
>
> For a current project [we](https://feinheit.ch/) needed a forms builder with the following constraints:
>
> - Simple fields (text, email, checkboxes, dropdowns etc.)
> - Custom validation and processing logic
> - It should be possible to add other content, e.g. headings and explanations between form fields
>
> The [form_designer](https://github.com/feincms/form_designer) fulfilled a few of these requirements but not all. It still works well but I wanted a forms builder based on [django-content-editor](https://github.com/matthiask/django-content-editor) for a long time already. Also, I really like the feincms3 pattern where the third party app only provides abstract models. Yeah, it is much more work to start with but the flexibility and configurability is worth it – especially since it's possible to write straightforward code to handle special cases[^2] instead of configuring even more settings.
>
> The humble beginnings are here in the [feincms3-forms](https://github.com/matthiask/feincms3-forms/) repository. The [test suite already shows how things work together](https://github.com/matthiask/feincms3-forms/tree/main/tests/testapp) but as of now no documentation exists and no release has been made yet. I hope it will be ready for a first beta release in the next few weeks 😄

Since then I have used feincms3-forms more often than form-designer, for building simple forms and also to build multi-step form wizards with custom fields, custom validation, configurable steps etc. The [README](https://github.com/feincms/feincms3-forms?tab=readme-ov-file#feincms3-forms) now actually explains why the project exists and how it could be used.

It still doesn't come close to WPForms in terms of included functionality; a big feature which is missing is conditional logic because I haven't yet had a use for it.

![The feincms3-forms admin interface](https://406.ch/assets/20240410-feincms3-forms.png)

The feincms3-forms forms support all types of content between form fields (basically everything [django-content-editor](https://django-content-editor.readthedocs.io/) supports). Plugins for form fields are more flexible and can add as many input fields to the form as they want, you're not restricted to single values or single input fields.
