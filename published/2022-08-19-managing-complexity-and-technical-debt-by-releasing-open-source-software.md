Title: Managing complexity and technical debt by releasing Open Source Software
Slug: managing-complexity-and-technical-debt-by-releasing-open-source-software
Date: 2022-08-19
Categories: Django, Programming

# Managing complexity and technical debt by releasing Open Source Software

When working on projects for [our](https://feinheit.ch) clients I often try to keep as much code as possible in third party packages; I often even create packages for Django apps even when I do not expect to use the code in more than one project at all. One of those packages (which, in the meantime _has_ been used more than once is [django-spark](https://django-spark.readthedocs.io/)).

At first sight it looks like more work to package, document and test the solution. Defining boundaries is also much harder when there are many packages involved -- it's not possible to just add a hack at the right place. You have to define extension points or hooks or you have to design a library which can be used in various ways -- there's not really a way around that when moving code into open source packages.

It isn't the case that this approach necessarily means more work though, neither in the initial project nor during [maintenance](https://406.ch/writing/low-maintenance-software/). Here's a list of reasons why that is:

- Once the logical units of functionality are identified separating them is relatively straightforward. Tricky pieces of code can be isolated, documented and tested using unit tests. I maintain that unit tests are more robust _and_ easier to write than integration tests.
- Moving code into Open Source packages keeps the packages themselves relatively clean of project-specific concerns. This means that the promise of reusability of Django's apps is actually achievable.
- Compatibility concerns aren't such a big topic. The third party package (initially) only has to work for the duration of the project.

There's never a guarantee that any open source library will be maintained in the future. I'm thinking that it may be useful to communicate the _intented maintenance_ better by adding an additional classifier when publishing a library. I'm thinking about something along these lines:

1. Actively maintained, used in multiple projects
2. Actively maintained, used in few projects which may even be in maintenance mode
3. Unmaintained right now, future maintenance is probable
4. Unmaintained right now, future maintenance is improbable
5. Definitely a dead project

But yeah, I'm not doing this classification work right now and haven't done it in the past. But it would certainly make it easier to know whether relying on a third party library is a good idea or not, as an additional signal to reading the code and skimming the issues and pull/merge requests.

<small>I have been sitting on this blog post for almost two years, and the ideas here have been gestating even longer. I'm sure someone else has said everything in here more eloquently in the meantime. But anyway, feedback is welcome as always and I don't think the post is so bad that it should sit in the draft folder forever.</small>
