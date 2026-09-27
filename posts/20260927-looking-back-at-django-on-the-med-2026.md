Title: Looking back at Django on the Med 🏖️  2026
Slug: looking-back-at-django-on-the-med-2026
Categories: Django, Programming
Draft: remove-this-to-publish

I haven't been to a programming conference in a really long time. That was mostly due to laziness, wanting to stay at home and decision fatigue because I didn't know how to travel sustainably and didn't know where to stay during the conference.

I had been talking online to Carlton for some time and when Django on the Med
🏖️  2026 was announced I knew I had to go. What's not to like about a
conference in Italy with all the good food and the mediterranean sea? I managed
to überwinden meinen inneren Schweinehund and reserved both the (free) ticket
for the conference itself and also the train ticket to go from Zurich to
Pescara. The train takes 8 or 9 hours depending on the connection with a single
change in Milano.

The conference itself consists only of development sprints and socialising -- no talks and nothing to prepare in advance for participants, except taking the computer with you and optionally having some ideas about what I want to work on.

## The import map Django Enhancement Proposal (DEP) I worked on

The forum discussion about [rejuvenating Django's `forms.Media`](https://forum.djangoproject.com/t/rejuvenating-vs-deprecating-form-media/21285) sparked my interest to revive Thibaud's DEP draft in early 2025. Some features which were mentioned in the early draft such as a `Stylesheet` object for including additional stylesheet attributes in `clasS Media` and CSP support have been added to Django in the meantime. My main motivation was and still is to bring import map support to Django. I have changed [django-prose-editor](https://pypi.org/project/django-prose-editor/) to use import maps in early 2025 and have written a first draft but then got stuck while trying to write a good DEP.

If all browsers were to support multiple import maps the DEP would maybe not be necessary. People could just ship an `ImportMap` media object and include it in `forms.Media(js=[...])` before the ES modules actually using it and things would just work. At the time of writing this post Chromium and Safari support multiple import maps but Firefox still doesn't So, if we want to use this feature without having import map merging we will have to wait several years for browser support being widespread enough. And since third party Django apps and Django websites which want to use import maps have to agree on a common implementation it makes most sense to me to propose adding this to Django core.

As an aside: Django has been famous for not having a frontend story for the longest time. I think this is mostly a strength, because Django has therefore allowed everyone to the frontend technologies they want and hasn't decided on a particular technology, library or framework which, in the meantime, would have become obsolete or not really state of the art. ES modules and import maps aren't opinionated in the same way for example jQuery, htmx, React or Svelte are, they really are a basic implementation of modules, namespaces and a specification how those modules should be loaded in the browser. So, I don't think it would be fair to reject adding better support for these things on the grounds that Django wants to be agnostic to the frontend. I'm not saying here that the DEP has to be accepted or that there cannot be good reasons to reject or modify it further -- I'm sure there are. I'm just proposing that we cannot just use the old arguments to argue against it.


## The diary

I'm now leaving the discussion of what I tried to achieve at the sprint and am concentrating instead on Django on the Med 🏖️ itself.

### Tuesday

On Tuesday morning I left home to take the train towards Pescara. I was really glad I packed my headphones with noise cancelation. After about 9 hours I arrived in the late afternoon, checked into the hotel, took m swimming trunks and immediately went to the beach.

In the evening we had a dinner at the seaside at Lido Aurora Pescara. It was a pleasure to finally meet some of the people I have been either working with or just following for a long time. A special surprise was mention Simon again. We met at Django under the hood in Amsterdam in 2016 and he has helped get my first pull request[^pr] to Django off the ground back then.

[^pr]: I have been contributing bug reports, tests and help much earlier than that but I was somewhat intimidated by Django's processes.

During the course of the conference we went back there several times. Good food, and luckily not just options with fish and sea food, but also good vegetarian options. (I'm not strictly vegetarian, but I sometimes prefer vegetarian or even vegan food.)

After a long day I slept surprisingly good. That's not saying much, but it certainly was a welcome surprise given my issues with my back and hips.


### Wednesday

The sprint officially started on wednesday with a warm up session led by Carlton. The three questions asked (paraphrased because I don't remember the exact wording) were "What is great about Django?", "What are the risks, or what could be better?" and "What are you planning to work on?"

I discussed waays of adding import maps with Joe, the author of for example [django-esm](https://github.com/codingjoe/django-esm). I thought we had completely different and conflicting ways of thinking about and using import maps. After talking it over it became clear quite quickly that, while we don't have to use them the same way, our ways of using them do not have to be in conflict. I think this is one of the big advnatages of events like this: The same discussion would have taken weeks or months in an issue tracker, if it ever happened, and in person it was a question of sitting together for an hour, hashing it out, and then you potentially have a basic agreement and an idea for which direction to go.

As already alluded to above I restarted my work on the DEP. It basically needed a complete rewrite since (excitingly!) so much has already landed in Django in the last ~18 months.

We went back to Lido Aurora for lunch. In the afternoon, almost everyone went for a bike ride a long an old railway track which has been converted into a bike lane along the sea. I already knew a similar thing from Liguria near Levanto/Bonassola but it was nice encountering it near Pescara again. (The new railway track has been built further inland.) We also had some nice Spritz abruzzese. Generally, Spritz isn't really my thing but those were a bit more bitter and earthy and less sweet and therefore we soon ordered a second round.

In the evening Žan, Annabelle, Simon, Carlton and myself went to Fruity Burger (or something like that) for some vegan food. As expected is was really tasty. While vegan options in restaurants can unfortunately sometimes be quite bland, vegan restaurants in my experience are often some of the best: You really have to know your ingredients and can't just add bacon to everything. (Nothing against bacon, but still.)


### Thursday

Again I started the day with a great coffee and an overly sweet breakfast (for my taste). Italian food is generally great but the breakfast isn't my thing. I like my müesli and whole grain bread. Anyway!

I continued working on the DEP and started tweaking [django-js-asset](https://github.com/feincms/django-js-asset) to serve as a proving ground and reference implementation for the ideas. Towards the end of thursday's sprint I had a first rough draft ready and Joe provided some great feedback on it. One of the most important points for me was to care about the API and not the implementation at this stage in the process. The DEP draft contained too much detail related to implementation and not enough examples showing of more complex use cases.

I only ate a small lunch since we were promised a bus tour with a lot of great food in the afternoon and evening. It still proved to be too much as we will learn later.

In the afternoon we took a bus to a local vineyard. We were shown around and had a look at the machines and learned a few things about the winemaking process. That was followed by a wine tasting and some bread and appetizers (XXX is that the correct word? Maybe antipasti would be more fitting? We had bread, thinly cut meat, a sauce made from cut up peppers in oil and some cheese)

Next, we went to Penne and were shown the city and were told a little bit of the local history. Everything's build from bricks. Brick buildings and earthquakes are not a great fit it seems to me -- the last larger earthquake hit th eregion less than 10 years ago. It's interesting that people are always rebuilding the houses anyway. From Penne we had a really nice view over the region, from the hill we were standing on all the way to Pescara and to the Adria.

We took the bus again to the resraurant and ate until 11 in the evening. At a certain point I couldn't go on anymore. No matter how great the food, there comes a moment when eating more seems impossible, and in my case that moment came before i Secondi. Also, I was in pain from too much sitting -- sitting isn't good since I'm still recovering from a disc hernia and the associated follow up issues in the hip. Still, I had a great day and wouldn't have wanted to miss any of it. The Secondi were arrosticini. I could only eat one so now I'm wondering if I am a persona non grata in Pescara 🤣.

Back in the hotel I couldn't sleep immediately so I addressed some of the feedback I got earlier in the day and then went to sleep.


### Friday

The night wasn't very restorative but I was awake anyway in the morning so I got up and started the day again on time. I finished applying the feedback to the DEP and to django-js-asset and continued refining it and filling in holes. I also modified some of the packages I'm developing to use the new way of defining media using import maps just to get a feeling if the API is nice or not.

During the coffee break I asked around if the changes to the way import maps are defined would break uses of the code. Luckily it seems that django-prose-editor seems to be "just used" and people weren't relying on being able to define import maps themselves yet. Or, if so, I don't know about it. Maybe [django-probe](https://djangoprobe.org/) could help with that, but we obviously aren't there yet.

We finished the sprint with a group picture and closed off the official part of the sprint. Most of us went out for lunch together. Some people had to leave after that; I drank an espresson in a nice coffee bar said goodbye to the people having to leave and went to the beach afterwards.

In the evening we went to an excellent vegan restaurant. I was happy that I wasn't the only one who was surprised to learn that the restaurant wasn't that close after all.


### Saturday

Almost everybody had either left or had to leave on Saturday morning so I didn't expect to meet with others anymore. I finally went for some long walks, explored other parts of the town and went to see the long bridge/walkway/passegio/whatever and some parks. I also took some time to note down both what we did and what I thought of finally going back to a conference.

In the evening I ran into Mark and Becky twice and we decided to have a beer together before saying goodbye again and for the final time for this sprint.

Having an additional day in Pescara was a win. I had less time to during the sprints to visit the city itself and really did appreciate the additional day I allowed myself to have.



## Finally

I'm wondering about the DEP process now and what happens with the pull requests I submitted. I'm linking to the [new feature ticket](https://github.com/django/new-features/issues/214), the [DEP pull request](https://github.com/django/deps/pull/101) and what I consider to be the [proving ground](https://github.com/feincms/django-js-asset) again. I have also mentioned above that it is the reference implementation, but due to the fact that django-js-asset has to be backwards compatible the real implementation may actually be quite a bit more simple.

I will be going back to Liguria, italy in just one week. Feels a bit stupid to cross the alps only to cross them again a few days later, but I'm really looking forward to sleeping in my own bed for a few days.

I can very well imagine going to more conferences and sprints again. The value of meeting in person is unquestionnable. It might be hard though on improving the experience we had here with the location, the nice weather and the social events. The selection of events is large and I won't be going to all of them certainly, but I am looking at going to the next Django on the Med in Malta, and maybe also to PyCon Italia and/or DjangoCon EU. We will see!
