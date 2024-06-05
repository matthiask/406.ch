Title: Weeknotes (2024 week 23)
Categories: Django, Programming, Weeknotes


## Switching everything from pip to uv

Enough said. I'm always astonished how fast computers can be.


## Releases

- [django-admin-ordering
  0.18](https://pypi.org/project/django-admin-ordering/): Added a database
  index to the ordering field since we're always sorting by it.
- [django-prose-editor 0.4](https://pypi.org/project/django-prose-editor/):
  Dropped the jQuery dependency making it possible to use the editor outside
  the Django administration interface without annoying JavaScript errors.
  Allowed additional heading levels and moved the block type buttons into a
  popover.
- [django-debug-toolbar 4.4.2](https://pypi.org/project/django-debug-toolbar/):
  I enjoy working on this important piece of software very much.
- [django-email-hosts 0.2.1](https://pypi.org/project/django-email-hosts/):
  Added a command analogous to ``./manage.py sendtestemail`` so that it's
  possible to easily test the different configured email backends.
- [feincms3 5.0](https://pypi.org/project/feincms3/): I completely reworked the
  move node action; previously it opened a new page where you could see all
  possible targets; now you can cut a page and paste it somewhere else. The
  advantages of the new interface is that you don't leave the changelist and
  can still profit from all its features while moving pages around.
- [feincms3-sites 0.21](https://pypi.org/project/feincms3-sites/): A new
  release taking advantage of a new hook in feincms3 7.0 so that the new moving
  interface works.
- [django-authlib 0.16.5](https://pypi.org/project/django-authlib/): authlib
  now shows a welcome message when authenticating using admin OAuth2. It's nice
  and helps with debugging strange authentication failures.
- [django-content-editor 7.0](https://pypi.org/project/django-content-editor/):
  I reworked the UI. The sidebar is gone, instead there are nice buttons in the
  place where you can add new plugins; the plugins appear in a nice grid
  instead of a list, which looks much better once you have more than just a few
  plugin types available. Also, plugin type icons are now shown in the plugin
  forms. I think it looks much better than before.
- [feincms3-cookiecontrol
  1.5.2](https://pypi.org/project/feincms3-cookiecontrol/): I didn't contribute
  anything to this release which is also a nice experience for a change. The
  Google consent mode integration has been improved and simplified.
- [django-json-schema-editor
  0.0.22](https://pypi.org/project/django-json-schema-editor/): Various
  small-ish improvements. I should really start using higher version numbers,
  but not having to commit to anything also feels great.  That being said, the
  editor is in active use in several projects, so maybe I'm deceiving myself.
