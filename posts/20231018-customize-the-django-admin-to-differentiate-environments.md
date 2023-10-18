Title: Customize the Django admin to differentiate environments
Date: 2023-10-18
Categories: Django, Programming
Draft: remove-this-to-publish

# Customize the Django admin to differentiate environments

We often have the same website running in different configurations:

- Once as a production site.
- Once as a place where editors update and preview the content. The content is later automatically (and maybe [partially](https://406.ch/writing/moving-data-including-deletions-between-the-same-django-app-running-in-different-environments/)) transferred from this environment to the production environment.
- Once as a stage environment to stabilize the code.
- And maybe additional environments for local development.

The Django admin panel mainly uses CSS variables for styling since [theming support was introduced in Django 3.2](https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#admin-theming) (by yours truly with a lot of help from others). This makes it simple and fun to customize the colors of all interface elements in a straightforward way without having to write loads of CSS.

If you have a `ENVIRONMENT` context variable available (as we do) you could add
the following template as `admin/base.html` to your project, giving you a red
color scheme for the production environment (to discourage people from updating
content) and a nice scheme for the `preproduction` environment which clearly
deviates from the standard color scheme used everywhere else:

    :::html+django
    {% block extrahead %}
      {{ block.super }}
      <style>
    #site-name::after {
      content: " ({{ ENVIRONMENT }})";
      font-size: 60%;
    }
      </style>
      {% if ENVIRONMENT == 'production' %}
        <style>
    :root {
      --primary: #aa0000;
      --secondary: #810000;
      --accent: yellow;
    }
        </style>
      {% elif ENVIRONMENT == 'preproduction' %}
        <style>
    :root {
      --primary: #30b181;
      --secondary: #1f7957;
      --accent: #cdffea;
    }
        </style>
      {% endif %}
    {% endblock %}
