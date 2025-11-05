Title: Weeknotes (2025 week 45)
Categories: Django, Programming, Weeknotes

## Autumn is nice

I love walking through the forest with all the colors and the rustling when you walk through the leaves on the ground.

## Updated packages since 2025-10-23

- [feincms3 5.4.3](https://pypi.org/project/feincms3/): Small fix for the
  YouTube IFRAME; it seems that the `referrerpolicy` attribute is now necessary
  for the embed to work everywhere.
- [django-json-schema-editor 0.8.2](https://pypi.org/project/django-json-schema-editor/):
  Allowed forwarding more options to the prose editor component; specifically,
  not just `extensions` but also the undocumented `js_modules` entry. This
  means that custom extensions are now also supported inside the JSON editor
  component.
- [django-prose-editor 0.20](https://pypi.org/project/django-prose-editor/):
  I reworked the menu extension to be customizable more easily (you can now specify [button groups and dropdowns](https://django-prose-editor.readthedocs.io/en/latest/menu.html#defining-button-groups-and-dropdowns) directly without using JavaScript code) and I also extended the [`NodeClass` extension](https://django-prose-editor.readthedocs.io/en/latest/nodeclass.html) to allow assigning predefined CSS classes not only to nodes but also to marks.
