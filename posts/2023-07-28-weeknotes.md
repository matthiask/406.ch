Title: Weeknotes (2023 week 30)
Date: 2023-07-28
Categories: Django, Programming, Weeknotes, feincms

# Weeknotes

## Async Django

I have used [Django Channels](https://channels.readthedocs.io/) successfully in a few projects from 2017 to 2019. A few months back I have worked with [Starlette](https://www.starlette.io/). And now I have finally started digging into using Django itself with an ASGI server, and not just for one or two views but also including the middleware stack etc since I also need authentication, not just an endpoint forwarding requests to a remote server. I have looked at [Granian](https://github.com/emmett-framework/granian), an RSGI/ASGI server written in Rust. But for now I am using [uvicorn](https://www.uvicorn.org/).

Django truly has come a long way but there's much left to do. Django 5.0 is looking great already, but 4.2 misses many pieces still. I am really really glad Django wants to stay backwards compatible but I wish I could wave a magic wand and upgrade everything to async. Adding `a` prefixes everywhere for the async version is certainly a good compromise and probably the way to go but it's just not that nice.

I have been playing around with making [feincms3](https://feincms3.readthedocs.io/)'s applications middleware async compatible because I want the full middleware stack to be async. The code is already released but undocumented and not even mentioned in the changelog. So, feel free to play around with it but it's not supposed to be stable or supported yet.

## Releases

- [feincms3 4.1](https://pypi.org/project/feincms3/): Switched to hatchling and ruff. Updated the feincms3-sites docs. Some async updates mentioned above. A Django 4.2 admin CSS update for the inline CKEditor.
- [feincms3-forms 0.4](https://pypi.org/project/feincms3-forms/): Switched to hatchling and ruff. Started defining default icons for the form fields [content editor](https://django-content-editor.readthedocs.io/) plugins.
- [django-ckeditor 6.7](https://pypi.org/project/django-ckeditor/): I'm still maintaining the CKEditor 4 integration for Django even though CKEditor 4 itself isn't supported anymore. Minor updates to the editor itself and Pillow compatibility updates.
- [feincms3-cookiecontrol 1.3.2](https://pypi.org/project/feincms3-cookiecontrol/): The cookie banner doesn't generate an empty `<div class="f3cc">` element anymore if there's nothing to add inside (e.g. if the user only accepted necessary cookies).
