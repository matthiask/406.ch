Title: LLMs for Open Source maintenance: a cautious case
Categories: Django, Programming
Draft: remove-this-to-publish

When ChatGPT appeared on the scene I was very annoyed at all the hype surrounding it. Since I'm working in the fast moving and low margin business of communication and campaigning agencies I'm surrounded by people eager to jump on the hype train when a tool promises to lessen the workload and take stuff from everyone's plate.

These discussions coupled with the fact that the training of these tools required unfathomable amounts of **stealing** were the reason for a big reluctance on my part when trying them out. I'm using the word stealing here on purpose, since that's exactly the crime [Aaron Swartz](https://en.wikipedia.org/wiki/Aaron_Swartz) [was accused of by the attorney's office of the district of Massachusetts](https://web.archive.org/web/20120526080523/http://www.justice.gov/usao/ma/news/2011/July/SwartzAaronPR.html). It's frustrating that some people can get away with the same crime when as soon as it is so much bigger. For example, OpenAI and Anthropic downloaded much more data than Aaron ever did.

A somewhat related thing happened with the too-big-to-fail banks: There, the people at the top were even compensated with [golden parachutes](https://en.wikipedia.org/wiki/Golden_parachute) at the end. LLM companies seem to be above accountability too.

Despite all this, I have slowly started integrating these tools into my workflows. I don't remember the exact point in time, but since some time in 2025 my opinions on their utility has started to change, at first grudgingly. At the beginning, I always removed the attribution and took great care to write and rewrite the code myself, only using the LLMs for inspiration and maybe to generate integration tests. More and more I have to say that they are useful, especially in projects with a clear focus and constraints.

Last week I fixed and/or closed all open issues in the [django-tree-queries](https://github.com/feincms/django-tree-queries) repository with the help of Claude Code. Is that a good thing? It could certainly be argued that it would have been better if I had done the work myself, but this doesn't take into account that I wouldn't have used the time and energy for that when I also want to do other things with my time than do Open Source work in the evening. I definitely also have leaned heavily on LLMs when working on [django-prose-editor](https://github.com/feincms/django-prose-editor).

So, we can produce more code, more features faster than before. Contrary to what people in my LinkedIn feed say that's clearly not an obviously good thing. But is it a race to the bottom where we drown in LLM-generated slop in quantities impossible to maintain? It doesn't feel like that. The tools have to get better faster than the amount of code they generate gets larger and larger. That's certainly a race which could go both ways. Throwaway code can be thrown away though, and well tested code does what the tests says therefore it's good according to my [rules for releasing open source software](https://406.ch/writing/my-rules-for-releasing-open-source-software/).

Regarding resource usage: It's certainly the case that we have coding agents which can be run locally with reasonable requirements (at least during inference, certainly not during training) and which do help close tickets faster, answer user inquiries faster and produce prototypes quicker.

Speaking as someone who has put more into the training set than they've taken out so far, I don't feel all that bad using the tools. Maybe that's rationalization. But contribution and profit needing to stay in some rough balance feels like the right frame — and total abstinence isn't the only ethical choice we have.
