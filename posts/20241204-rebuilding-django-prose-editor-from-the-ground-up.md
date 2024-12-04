Title: Rebuilding django-prose-editor from the ground up
Categories: Django, Programming


The [django-prose-editor](https://pypi.org/project/django-prose-editor/) package provides a HTML editor based upon the [ProseMirror toolkit](https://prosemirror.net/) for the Django administration interface and for the frontend.

The package has been extracted from a customer project and open sourced so that it could be used in other projects as well. It followed a very restricted view of how rich text editors should work, which I have initially added to the [FeinCMS repository when documenting the design decisions more than 15 years ago](https://github.com/feincms/feincms/commit/70cd7a1244438d2ba97852256f77daa2c870c345#diff-556c5559a716059d4fb714ad34de6a9845870e8d55bbd2cb9d77c732eb961388) <small>(Note that I didn't edit the paragraph, it's reproduced here as it was back then, with all the errors and heedlessness.)</small>

> All of this convinced me that offering the user a rich text editor with too much capabilites is a really bad idea. The rich text editor in FeinCMS only has bold, italic, bullets, link and headlines activated (and the HTML code button, because that's sort of inevitable -- sometimes the rich text editor messes up and you cannot fix it other than going directly into the HTML code. Plus, if someone really knows what he's doing, I'd still like to give him the power to shot his own foot).

My personal views are unchanged. I have to recognize though that forcing this idea upon everyone isn't workable and that this would mean that I'd have to find a different editor for most projects just because people really want or need more rope. Going back to an editor which allows everything was out of the question, so I had to look around for a way to allow project-specific extensions for the editor.

Of course that's problematic, since Django packages and Python virtualenvs do not offer a good way of shipping CSS and JavaScript which should be available for a frontend bundler to process. The existing [Django staticfiles app](https://docs.djangoproject.com/en/5.1/ref/contrib/staticfiles/) is great, works well, but it's not a bundler -- and it shouldn't be.

So, I started shopping around for ways to make ProseMirror extensible while keeping extensions clean and well localized. Instead of inventing another plugin ecosystem I settled on [Tiptap](https://tiptap.dev/) which uses ProseMirror under the hood. The abstractions are pleasantly leaky -- if you know how to work with ProseMirror's API, you can use Tiptap's API without any issues. That was important for me, since I already have a somewhat large selection of plugins which I do not want to reimplement from the ground up.

I had already looked at Tiptap a few years back, but ultimately stayed with ProseMirror because I liked some behaviors better (such as not including trailing spaces in marks) and because I didn't need the extensibility which at the time only made the resulting bundle much bigger.

Now, things have improved a lot, and I'm really happy with Tiptap and the development version of django-prose-editor. [Writing an editor extension in project code is great](https://github.com/matthiask/django-prose-editor/?tab=readme-ov-file#customization), and my editor core stays nice. Also the list of readily available extensions is large, and most of the things just work.
