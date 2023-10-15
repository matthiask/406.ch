Title: Why we switched from Slack to Discord at Work
Date: 2023-10-15
Categories: Programming

We have switched from Slack to Discord at [Feinheit](https://feinheit.ch) a few years back. This post explores the history, the reasons for the switch and what we learned in the meantime.

## The early days

In the early days we used Skype group chats. I don't remember why we stopped.
We probably became too numerous for a single chat. After we stopped we
certainly missed the easy way to share things with everyone. An alternative had
to be found. Company based social networks were the hype for a short amount of
time. I don't even remember the name of the product we used, that probably says
enough about that. Suffice to say that it wasn't a happy time tool-wise.

## Slack

Then came Slack. Finally we had something easy to use, again. Need a new space to
discuss something? Just open a new channel, everybody can do it! Need to ask a
specific person something? Direct messages are right there, and (arguably) much
better than always interrupting people by walking to their desk for everything.

However, my personal lived experience rapidly deteriorated. I wanted to be
accessible for urgent inquiries to unblock colleagues when they needed
something. But this also fostered an ASAP culture. Project managers knew I was
almost always available. It didn't help that some were terribly unorganized at
times.

Since asking was easier that searching the documentation or the handbook people
didn't bother to document things anymore. The information was shared in Slack
but since nobody found the relevant messages after time had passed the same
questions were asked (and answered) over and over. Slack became the place where
knowledge goes to die.

After a time Slack became my primary source of stress. I tried several times to
stop using it. I suffered an unreasonable amount of FOMO[^fomo] during that
time but it was also true that I did not know stuff which was only shared on
Slack by others. I asked myself many times what my problem was and why I
couldn't "simply" shut it off and ignore the downsides. And a minor but still
important point, ignore the unread messages indicator.

[^fomo]: Fear Of Missing Out.

Luckily I learned of others who felt the same way, mostly outside the company
but some of them at Feinheit. Slack had to go. The question was: Which tool
could be a suitable replacement? Given the title of this post it shouldn't come
as a surprise that the answer was Discord.

## Digression: Project management software

It's probably important to know that we have been using a project management
tool and also issue trackers all this time. So, Slack really wasn't just a
possibly improved[^1] replacement for mail-based project management. Slack
mainly crept into the project management tooling because some people perceived
it to be more modern: A simpler way for those asking others for their time or
knowledge.

[^1]: For some people it seems to be an improvement.

## Discord as an addition, not a replacement for project management software

We have started using Discord in the summer of 2021 with a clear set of rules
and a small number of channels.

### Rules

The most important rules are:

- Discord is the place for casual and informal exchange.
- Nobody is expected to read anything on Discord. If it is expected that people
  actually receive a message it must not be shared on Discord.
- No discussing project work, not in channels nor in direct messages. The
  former is enforced by a short list of moderators, the latter is formulated as
  an expectation (since it's impossible to enforce).

The rules message also contains a direct message to a shared to do list, where
everyone can easily assign to do items to others without having to find the
project's issue tracker. This is especially important because we have many
small projects and no one works on all of them. If assigning to dos wasn't
relatively straightforward people would understandably fall back to direct
messages.

### Server configuration

We are able to uphold these rules because of Discord's strong moderation
features (compared to Slack). Discord is much more configurable. Our server is
configured in the following way:

- Channel creation is disallowed. Only moderators can create new channels; if
  someone asks for a new channel, the request is denied if it is probable that
  the rules above would be broken.
- No one is expected to accept DMs from other members.
- Threads are disabled. The structure they provide makes it acceptable to loop
  people into a "quick" conversation which 99% of the time belongs somewhere
  more permanent, for example the project management software.

Those are just the most important points.

### Channels

At the time of writing those are our text channels (The names are translated to their equivalents):

- `#reception` -- this is the only channel people see when they haven't been
  given the appropriate role. This is necessary because everybody can join a
  server if they have an invite code and we don't want random people to read
  everything we post.
- `#staircase` -- the place to say hello, bye, and a few things in-between.
- `#random` -- all servers need this :-)
- `#politics` -- a separate space for politics. Everything's political, and we are too.
- `#inspiration` -- I myself thought that `#staircase` and `#random` would be
  sufficient but people wanted this and the moderators didn't think that this
  additional channel would lead to a violation of the rules above.

Additionally, we have two voice channels, `cow-orking` and `sofa`. The former
was used more ofting when more people were working from home to have a place to
hear from others, the latter is more an invitation to talk. More talk happens
in-person in the office these days, but when working remotely it's still nice
to know that those channels are just a click away.

## Closing words

I myself have joined the work discord using my private account and I feel good
about that. I'm not friends with everyone at work but I certainly have good
relationships with basically everyone.

I also did not live-stream my activities to Discord before creating the work
server anyway so there hasn't been a change there at all. And people mostly
know that Discord is about the slowest place to get something from me (and I
make a point of it!) so even if people do not heed the "No DMs" rule above this
behavior isn't really reinforced.

I'm actually really happy with the way we're using these tools these days.
