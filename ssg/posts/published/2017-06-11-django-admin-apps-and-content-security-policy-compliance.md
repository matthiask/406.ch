Title: Django admin apps and Content Security Policy compliance
Slug: django-admin-apps-and-content-security-policy-compliance
Date: 2017-06-11
Categories: Django, Programming
Type: markdown

# Django admin apps and Content Security Policy compliance

Since Django 1.10 the bundled admin app [does not use inline JavaScript anymore](https://github.com/django/django/commit/d638cdc42acec608c1967f44af6be32a477c239f).
This means that a vanilla installation of `django.contrib.admin`
without any additional apps (and additional functionality) would
already be [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) (CSP) compliant.

However, most – if not all – of our projects use apps that need to load additional JavaScript. Of course overriding templates is easy, and adding <code>&lt;script&gt;</code> tags as well, but this approach quickly leads to duplicated code in our projects. It got a little bit better since Django supports extending templates recursively, but I don’t really want to debug this if things go wrong.

An example for such an app is [django-admin-ordering](https://github.com/matthiask/django-admin-ordering/), an app which adds drag-drop reordering to inlines and changelists. The JavaScript code has to know the name of the ordering field and the name of inlines. [django-js-asset](https://github.com/matthiask/django-js-asset/) provides a straightforward way of passing those attributes to the JavaScript code without having to override any templates, which helps [keeping maintenance low](/writing/low-maintenance-software/). The app (ab)uses the `forms.Media`
container to also add data attributes to script tags.
Those data attributes only contain JSON which (according to my understanding of CSP) is safe.

Instead of this:

    forms.Media(js=["admin_ordering/admin_ordering.js"])

... we do this:

    from js_asset import JS
    forms.Media(js=[
        JS(
            "admin_ordering/admin_ordering.js",
            {
                "data-admin-ordering": json.dumps(…).
            },
        )
    ])

And in the JavaScript code itself we can access the data using:

    let el = document.querySelector("[data-admin-ordering]"),
    	ctx = JSON.parse(el.dataset.adminOrdering)

The django-js-asset package is available on [Github](https://github.com/matthiask/django-js-asset/) and [PyPI](https://pypi.python.org/pypi/django-js-asset).

(Updated in August 2017 to avoid using internal API of `forms.Media` which will be removed in Django 2.0.)
