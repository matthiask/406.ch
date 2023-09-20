Title: Keep content managers' admin access up-to-date with role-based permissions
Date: 2023-09-20
Categories: Django, Programming, feincms

# Keep content managers' Django admin access up-to-date with role-based permissions

[Django's built-in permissions
system](https://docs.djangoproject.com/en/4.2/topics/auth/default/#permissions-and-authorization)
is great if you want fine-grained control of the permissions content
managers should have. The allowlist-based approach where users have no
permissions by default and must be granted each permission individually makes a
lot of sense to me and is easy to understand.

When we build a CMS at [Feinheit](https://feinheit.ch/) we often use the Django administration panel as a CMS.
Unfortunately, Django doesn't provide a way to specify that content managers
should have all permissions in the `pages` and `articles` app (just as an
example). Adding all current permissions in a particular app is straightforward when using the
[`filter_horizontal`](https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.filter_horizontal)
interface but keeping the list up-to-date later isn't. When we add an
additional [content block
plugin](https://406.ch/writing/my-reaction-to-the-block-driven-cms-blog-post/)
we always have to remember to also update the permissions after deploying the
change -- and often, deployment happens some time after the code has been
written, e.g. because clients want to approve the change first. What happens
all too often is that the manual step of updating permissions gets forgotten.

This has annoyed me (intermittently) for a long time and my preferred solution
has always been to give superuser permissions to everyone and trust them to
not make changes which they aren't supposed to according to the _Trusted Users
Editing Structured Content_ principle which was mentioned in a Django book I
read early in my Django journey.

## The basic ideas of my role-based permissions implementation

A recent project has resurfaced this annoyance and I did finally bite the
bullet and implement a solution for this in the form of a
[django-authlib](https://github.com/matthiask/django-authlib/) extension. The basic ideas are:

**All users are assigned a single role**: Single roles sound inflexible, but is
good enough for my default use case. Examples for roles could be _default_ (no
additional permissions granted), _content managers_ (grant access to the pages
and articles apps) or maybe _deny auth_ (deny access to users, groups and
permissions).

**The permission check is implemented using a single callable**: A custom
backend is provided whose only job is to call the correct callable for the
user's current role.

**The callable either returns a boolean or raises `PermissionDenied` to prevent
other backends from granting access**: No new ideas here, it's exactly what
[Django's authentication backends are supposed to
do](https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#handling-authorization-in-custom-backends).

**Permission checkers for the most common scenarios are bundled**:
django-authlib only ships one permission checker right now, `allow_deny_globs`,
which allows specifying a list of permission name globs to allow and to deny.
Deny overrides allow as is probably expected.

## Using roles in your own project

Specify the available roles in your settings and add the authentication backend:

    :::python
    from functools import partial
    from authlib.roles import allow_deny_globs
    from django.utils.translation import gettext_lazy as _

    AUTHLIB_ROLES = {
        "default": {"title": _("default")},
        "staff": {
            "title": _("editorial staff"),
            "callback": partial(
                allow_deny_globs,
                allow={
                    "pages.*",
                    "articles.*",
                },
            ),
        },
    }

    AUTHENTICATION_BACKENDS = (
        # This is the necessary additional backend
        "authlib.backends.PermissionsBackend",
        # Maybe you want to use authlib's email authentication ...
        "authlib.backends.EmailBackend",
        # ... or the standard username & password combination:
        "django.contrib.auth.backends.ModelBackend",
    )

You have to extend your user model (you have to use [a custom user model](https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#specifying-custom-user-model) if you're not using django-authlib's `little_user.User`):

    :::python
    from authlib.roles import RoleField

    class User(AbstractUser):
        # ...
        role = RoleField()

And that's basically it.

Of course the globbing is flexible, you could also allow users to view all objects:

    :::python
    partial(allow_deny_globs, allow={"*.view_*"})

Or you could block users from deleting anything:

    :::python
    partial(allow_deny_globs, deny={"*.delete_*"})

And as mentioned above, you can also combine `allow` and `deny` (`deny` wins
over `allow`) or even provide your own callables. If you provide your own
callable it must accept `user`, `perm` and `obj` (which may be `None`) as
keyword arguments. Implementing such a callable is probably less work than
implementing an authentication backend yourself; I had to do more work than
initially expected because only implementing `.has_perm` isn't sufficient if
you want to see any apps and models in the admin index page. The current
`allow_deny_globs` implementation is nice and short:

    :::python
    def allow_deny_globs(user, perm, obj, allow=(), deny=()):
        for rule in deny:
            if fnmatch(perm, rule):
                raise PermissionDenied
        return any(fnmatch(perm, rule) for rule in allow)
