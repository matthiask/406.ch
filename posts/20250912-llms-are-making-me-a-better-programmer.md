Title: LLMs are making me a better programmer...
Categories: Django, Programming

I'm still undecided about LLMs for programming. Sometimes they are very useful, especially when working on a clearly stated problem within a delimited area. Cleaning the code up afterwards is painful and takes a long time though. Even for small changes I'm unsure if using LLMs is a way to save (any) resources, be it time, water, energy or whatever.

They do help me get started, and help me be more ambitious. That's not a new idea. [Simon Willison wrote a post about this in 2023](https://simonwillison.net/2023/Mar/27/ai-enhanced-development/) and the more I think about it or work with AI the more I think it's a good way to look at it.

A recent example which comes to mind is writing end to end tests. I can't say I had a love-hate relationship with end to end testing, it was mostly a hate-hate relationship. I hate writing them because it's so tedious and I hate debugging them because of all the timing issues and the general flakyness of end to end testing. And I especially hate the fact that those tests break all the time when changing the code, even when changes are mostly unrelated.

When I discovered that I could just use Claude Code to write those end to end tests I was ecstatic. Finally a way to add relevant tests to some of my open source projects without having to do all this annoying work myself! Unfortunately, I quickly discovered that Claude Code decided (ha!) it's more important to make tests pass than actually exercising the functionality in question. When some HTML/JavaScript widget wouldn't initialize, why not just manipulate `innerHTML` so that the DOM looks as if the JavaScript actually ran? Of course, that's a completely useless test. The amount of prodding and instructing the LLM agent required to stop adding workarounds and fallbacks everywhere was mindboggling. Also, since tests are also code which has to be maintained in the future, does generating a whole lot of code actually help or not? Of course, the amount of code involved wasn't exactly a big help when I really had to dig into the code to debug a gnarly issue, and the way the test was written didn't exactly help!

I didn't want to go back to the previous state of things when I had only backend tests though, so I had to find a better way.

## Playwright codegen to the rescue

I already had some experience with [Playwright codegen](https://playwright.dev/docs/codegen-intro), having used it for testing some complex onboarding code for a client project I worked on a few years back, so I was already aware of the fact that I could run the browser, click through the interface myself, and playwright would actually generate some of the required Python code for the test itself.

This worked fine for a project, but what about libraries? There, I generally do not have a full project ready to be used with `./manage.py runserver` and Playwright. So, I needed a different solution: Running Playwright from inside a test!

If your test uses the [`LiveServerTestCase`](https://docs.djangoproject.com/en/5.2/topics/testing/tools/#django.test.LiveServerTestCase) all you have to do is insert the following lines into the body of your test, directly after creating the necessary data in the database (using fixtures, or probably better yet using something like [factory-boy](https://pypi.org/project/factory-boy/)):

    :::python
    import subprocess
    print(f"Live server URL: {live_server.url}")
    subprocess.Popen(["playwright", "codegen", f"{self.live_server_url}/admin/"])
    input("Press Enter when done with codegen...")

Or of course the equivalent invocation using `live_server.url` when using the `live_server` fixture from [pytest-django](https://pytest-django.readthedocs.io/en/latest/helpers.html#live-server).

Of course Tim [pointed me towards `page.pause()`](https://mastodon.social/@CodenameTim/115096138737981083). I didn't know about it; I think it's even better than what I discovered, so I'm probably going to use that one instead. I still think writing down the discovery process makes sense.

So now, when `LiveServerTestCase` is already set up and I already have a sync Playwright context lying around, I can just do:

    :::python
    page = context.new_page()
    page.pause()

## TLDR

Claude Code helped getting me to get off the ground with adding end to end tests to my projects. Now, my tests are better because -- at least for now -- I'm not using AI tools anymore.
