Title: Workbench: Coffee time!
Categories: Django, Programming

# Workbench: Coffee time!

I have written about [the Workbench agency
software](https://406.ch/writing/workbench-the-django-based-agency-software/) a
few weeks back.

Back when we were using Slack at [Feinheit](https://feinheit.ch/) we used a
Donut bot to generate randomized invites for a coffee break. [We lost that bot
when we switched to
Discord](https://406.ch/writing/why-we-switched-from-slack-to-discord-at-work/).
I searched some time for an equivalent bot for Discord but couldn't find any,
so like any self-respecting nerd, break lover and NIH-sufferer I reimplemented
the functionality as a part of our agency software.

The first version generated totally random pairings without any history; I
thought that maybe this would be good enough, but of course I received an
invite for a coffee with the exact same person in the first two invitations.
Even though I did enjoy the break both times this motivated me to put some
effort into a better solution :-)

The result of this work is the [`coffee_invites()` function](https://github.com/matthiask/workbench/blob/a14d8b9560def7a4e2bbf7531eb6108f734568db/workbench/accounts/tasks.py#L57)

There are two main parts to the generator:

- It randomly generates twenty pairings from all participants; it prefers
  groups of two except for the last group which may contain three people.
- It loads old pairings from the database and gives higher penalties to equal
  pairings depending on the time which has passed since the last time.

So, it's not mathematically perfect, but all imbalances will cancel out over a
long time. I experimented with the discounting factor and the number of random
pairings it generates upfront. The values in the code seem to work fine.

Sometimes it's simple stuff like this which gets me going and reignites the
love for programming. Like a small puzzle.
