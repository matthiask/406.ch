Title: Composition over inheritance: The case for function-based views
Date: 2023-08-02
Categories: Django, Python, Programming, feincms
Draft: remove-this-to-publish

# Composition over inheritance: The case for function-based views

[A recent conversation with Carlton on Mastodon](https://hachyderm.io/@matthiask/110814846128940975) prompted me to write down a summary of my thoughts re. function- vs class-based views in Django.

## The early days

When I started using Django some time after 0.96 and 1.0 all views were
function based. Except when you added a class with a `def __call__()` method
yourself -- that was always possible but not really comparable to today's
class-based views.

## The introduction of class-based views

Class based views (both generic versions and the base `View`) were introduced to Django in 2010. Judging from the [ticket tracker](https://code.djangoproject.com/ticket/6735) the main motivation was to avoid adding yet another argument to the generic function-based views (GFBV) which we're available in Django back then.

The GFBV's argument count was impressive. Two examples follow:

    :::python
    def object_detail(request, queryset, object_id=None, slug=None,
        slug_field='slug', template_name=None, template_name_field=None,
        template_loader=loader, extra_context=None,
        context_processors=None, template_object_name='object',
        mimetype=None):
        ...

    def archive_month(request, year, month, queryset, date_field,
        month_format='%b', template_name=None, template_loader=loader,
        extra_context=None, allow_empty=False, context_processors=None,
        template_object_name='object', mimetype=None, allow_future=False):
        ...

The GFBVs where immediately when GCBVs were introduced and later removed in 2012.

The class-based views introduced a few patterns such as:

- Class-based views have to be adapted by calling the `View.as_view()` method; `as_view()` returns arguably the thing which is viewed (sorry) as the view by Django, it's the thing which gets called with a request and is expected to return a response.
- This thing instantiates the view object once per request; this means that `self` can be used to save request-specific data such as `self.request`, `self.args` but also custom attributes.

The GCBV code is extremely factored and decomposed. The [Classy Class-Based Views](https://ccbv.co,ul/) site mentions that the `UpdateView` has 10 separate ancestors and its code is spread across three files. But, the view code for instantiating a model object and handling a form really isn't that complex. Most of the complexity is handled by Django itself, in the request handler and in the `django.forms` package. So, what's the reason for all this?

## Generic views could be simple

I wish that the existing generic views had better building blocks instead of a big hierarchy of mixins and multiple inheritance which is probably not understood by anyone without checking and re-checking the documentation, the code, or the excellent [Classy Class-Based Views](https://ccbv.co.uk/). Certainly not by me.

In my ideal world, generic views would be composed of small reusable and composable functions where you could copy the code of the view, change a line or two, and leave it at that. And since the functions do one thing (but do that well) you can immediately see what they are doing and why. And you avoid adding too much of the Hollywood Principle (Don't call us, we'll call you) in your code. Sure, your view is called by Django, but you don't have to introduce more and more layers of indirection.

The internet is full of advice that you should prefer composition over inheritance. Let's try to outline what generic views could look like if they followed the composition paradigm. Note that the goal isn't to gain points by showing that the resulting code is shorter -- the goal is maintainability by being easier to understand, and by showing a better path from a beginner's use of views to an experts understanding of everything underneath it.

Before refactoring and following DRY (Don't Repeat Yourself) to the extreme you should instead follow the [Three Strikes And You Refactor](https://wiki.c2.com/?ThreeStrikesAndYouRefactor) rule[^wet]. Some repetition is fine. Not all identical three lines of code are the same.

[^wet]: Also called the WET rule (Write Everything Twice). (Not coined by me.)

### ListView and DetailView

I'm going to profit from [feincms3's shortcuts module](https://feincms3.readthedocs.io/en/latest/ref/shortcuts.html) which offers functions for rendering pages for single objects or lists of objects. The `render_list` and `render_detail` functions implement the same way of determining the template paths as the generic views use (for example `<app_name>/<model_name>_detail.html`) and the same way of naming context variables (`object` and `<model_name>` for the object, `object_list` and `<model_name>_list` for the list) as well as pagination, but nothing more.

Here's a possible minimal implementation of a list and detail object generic view:

    :::python
    # _get_queryset runs ._default_manager.all() on models and returns
    # everything else as-is. It's the secret sauce which allows using models,
    # managers or querysets with get_object_or_404 and friends.
    from django.shortcuts import get_object_or_404, _get_queryset
    from feincms3.shortcuts import render_list, render_detail

    def object_list(request, *, model, paginate_by=None):
        return render_list(request, _get_queryset(model), paginate_by=paginate_by)

    def object_detail(request, *, model, slug, slug_field="slug"):
        object = get_object_or_404(model, **{slug_field: slug})
        return render_detail(request, object)

You want to change the way a single object is retrieved? You could do that easily, but not by adding configuration-adjacent values in your URLconf but rather by adding a view yourself:

    :::python
    def article_detail(request, year, slug):
        object = get_object_or_404(Article.objects.published(), year=year, slug=slug)
        return render_detail(request, object)

    urlpatterns = [
        ...
        path("articles/<year:int>/<slug:slug>/", article_detail, name=...),
        ...
    ]

I don't think that was much harder than a hypothetical alternative:

    :::python
    urlpatterns = [
        ...
        path(
            "articles/<year:int>/<slug:slug>/",
            object_detail,
            {
                "model": Article.objects.published(),
                "object_kwargs": ["year", "slug"],
            },
        ),
        ...
    ]

And think about the internal implementation of the `object_detail` view. Viewed one additional feature at a time it may be fine, but when adding up everything it would probably be quite gross.

The additional benefit is that it shows beginners the way to intermediate skills -- writing views isn't hard, and shouldn't be.

Finally, the official way of overriding `DetailView.get_object()` (I think!) doesn't look that good compared to the `def article_detail()` view above:

    :::python
    class ArticleDetailView(generic.DetailView):
        def get_object(self, queryset=None):
            if queryset is None:
                queryset = self.get_queryset()
            return get_object_or_404(queryset, year=self.kwargs["year"], slug=self.kwargs["slug"])

Did you know that `get_object()` has an optional queryset argument? I certainly didn't. It seems to be used by the date-based generic views, but they also have their own `get_object()` implementation so who knows, really.

## Detail view with additional behavior

    :::python
    def article_detail(request, year, slug):
        object = get_object_or_404(Article.objects.published(), year=year, slug=slug)
        data = (request.POST, request.FILES) if request.method == "POST" else ()
        form = CommentForm(*data, comment=object)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(".#comments")
        return render_detail(request, object, {"comment_form": form})

A counterexample would be to move the endpoint which accepts a comment POST
request somewhere else. But then you'd also have to keep the different
`CommentForm` instantiations in sync.

You could also override `get_context_data()` to add the comment form to the
context and override `post()` to instantiate check the form's validity. But
then you'd have to make sure that an eventual invalid form is handled correctly
by `get_context_data()`. It's not hard but it certainly isn't as
straightforward as the example above either.

The custom view is the most obvious way of keeping the form instantiation in
one place.

## Form views

Generic create and update views could look something like this, again reusing the shortcuts mentioned above:

    :::python
    def save_and_redirect_to_object(request, form):
        object = form.save()
        return redirect(object)

    def get_form_instance(request, *, model, form_class, instance=None):
        assert model or form_class, "Provide at least one of model and form_class"
        if form_class is None:
            form_class = modelform_factory(model)
        data = (request.POST, request.FILES) if request.method == "POST" else ()
        return form_class(*data)

    def object_create(request, *, model=None, form_class=None, form_valid=save_and_redirect_to_object):
        form = get_form_instance(request, model=model, form_class=form_class)
        if form.is_valid():
            return form_valid(request, form)
        return render_detail(request, form.instance, {"form": form}, template_name_suffix="_form")

    def object_update(request, *, model, slug, slug_field="slug", form_class=None, form_valid=save_and_redirect_to_object):
        object = get_object_or_404(model, **{slug_field: slug})
        form = get_form_instance(request, model=object.__class__, form_class=form_class, instance=object)
        if form.is_valid():
            return form_valid(request, form)
        return render_detail(request, form.instance, {"form": form}, template_name_suffix="_form")

You want to redirect to a different URL and maybe emit a success message? Easy:

    :::python
    def article_form_valid(request, form):
        form.save()
        messages.success(request, _("Successfully updated the article."))
        return redirect("articles:list")

    urlpatterns = [
        ...
        path(
            "<slug:slug>/update/",
            object_update,
            {"model": Article, "form_valid": article_form_valid},
            name=...
        ),
        ...
    ]

Yes, these generic views wouldn't allow overriding the case when a form was invalid. But, I'd assume that displaying the form with error messages is the right thing to do in 90% of the cases. And if not, write your own specific or generic view? After all, with the mentioned tools it won't take up more than a few lines of straightforward code. (If the code was tricky it would be different. But views shouldn't be tricky.)

## Date-based generic views

I think I would want to offer a few analyzers which allow easily returning a
data structure suitable for rendering links for yearly, monthly, weekly or even
daily (who writes that much?) archives. The [`.dates()` queryset
method](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#dates)
method should be a big help there.

The archive views themselves are straightforward adaptations of the
`object_list` view above.

It may feel like leaving out the actually hard part, but I'd have to be
convinced that this is actually a hard problem and not just a problem of making
basically arbitrary choices which people then adapt to and then think that this
is the way things should be since it's the way things are.

## Wrapping up

Some points this post could have made or tried to make are made much better by
Luke Plant in the guide [Django Views - The Right
Way](https://spookylukey.github.io/django-views-the-right-way/). I don't
generally think that class-based views never make sense. I also don't think
that people shouldn't use the available tools. I just think that I, myself,
don't want to use them, and I also think that I'm still happier with `lambda
request: HttpResponseRedirect(...)` than with
`generic.RedirectView.as_view(url=...)`. The point isn't to compare the
character count. The point is: Does the `RedirectView` cause a permanent or a
temporary redirect? I had to look it up for a long time, and then it changed.
The former is completely obvious.

## Closing words

I know that people have strong opinions. I'm not interested in all of them. I'm
mostly interested in design critiques and arguments regarding the beginner to
intermediate skills argument. It's fine if CBVs work fine for you, and there's
no need to feel challenged by this post. Thanks for reading.
