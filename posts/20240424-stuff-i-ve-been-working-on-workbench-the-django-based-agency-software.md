Title: Workbench, the Django-based agency software
Categories: Django, Programming

I get the impression that there's a lot of interesting but unknown software in Django land. I don't know if there's any interest in some of the packages I have been working on; if not this blog post is for myself only.

## (Hi)story time

As people may know I work at [Feinheit](https://feinheit.ch/), an agency which specializes in digital communication services for SMEs, campaigns for referendums, and website and webapp development. At the time of writing we are a team of about 20-25 communication experts, graphic designers, programmers and project managers.

We have many different clients and are working on many different projects at the same time and are billing by the hour[^bythehour]. Last year my own work has been billed to more than 50 different customers. In the early days we used a shared file server with spreadsheet files to track our working hours. Luckily we didn't often overwrite the edits others made but that was definitely something which happened from time to time.

[^bythehour]: Rather, in six minute increments. It's even worse.

We knew of another agency who had the same problems and used a FileMaker-based software. Their solution had several problems, among them the fact that it became hard to evolve and that it got slower and slower as more and more data was entered into it over the years. They had the accounting know how and we had the software engineering know how so we wrote a webapp based on the Django framework. As always, it was much more work than the initial estimate, but if we as programmers didn't underestimate the effort needed we wouldn't have started many of the great projects we're now getting much value and/or enjoyment from, hopefully both. The product of that work was [Metronom](https://www.fineware.ch/). The first release happened a little bit later than [harvest](https://www.getharvest.com/about) but it already came with full time tracking including an annual working time calculator, absence management, offers, invoices including PDF generation etc, so it was quite a bit more versatile while still being easier to use than "real" business software solutions.

I personally was of the opinion that the product was good enough to try selling it, but for a variety of reasons (which I don't want to go into here) this never happened and [we](https://feinheit.ch/) decided that we didn't want to be involved anymore.

However, this meant that we were dead-end street with a software that didn't belong to us anymore, which wasn't evolving to our changing requirements. I also didn't enjoy working on it anymore. Over the years I have tried replacing it several times but that never came to pass until some time after the introduction of [Holacracy](https://www.holacracy.org/) at our company. I noticed that I didn't have to persuade everyone but that I, as the responsible person for this particular decision, could "just"[^just] move ahead with a broad interpretation of the purpose and accountabilities of one of my roles.

[^just]: Of course it's never that simple, because the responsibility is a lot. The important point is: It would have been a lot of work anyways, the big difference is that it was sufficient to get consent from people; no consensus required.

## [Workbench](https://github.com/matthiask/workbench)

![Screenshot](https://406.ch/assets/20240424-workbench.png)

[Workbench](https://github.com/matthiask/workbench) is the product of a few long nights of hacking. The project was started as an experiment in 2015 and was used for sending invoices but that wasn't really the intended purpose. After long periods of lying dormant I have brought the project to a good enough state and switched Feinheit away from Metronom in 2019.

I have thought long and hard about switching to one of the off-the-shelf products and it could very well be that one of them would work well for us. Also, we wouldn't have to pay (in form of working hours) for the maintenance and for enhancements ourselves. On the other hand, we can use a tool which is tailored to our needs. Is it worth the effort? That's always hard to answer. The tool certainly works well for the few companies which are using it right now, so there's no reason to agonize over that.

At the time of writing, Workbench offers projects and services, offers and invoices incl. PDF generation, recurring invoices, an address book, a logbook for rendered services, annual working time reports, an acquisition funnel, a stupid project planning and resource management tool and various reports. It has not only replaced Metronom but also a selection of SaaS (for example Pipedrive and TeamGantt) we were using previously.

The whole thing is open source because I don't want to try making agency software into a business anymore, I only want to solve the problems *we* have. That being said, if someone else finds it useful then that's certainly alright as well.

The license has been MIT for the first few years but I have switched to the GPL because I wanted to integrate the excellent [qrbill](https://pypi.org/project/qrbill/) module which is also licensed under the GPL. As I wrote elsewhere, I have released almost everything under the GPL in my first few open source years but have switched to BSD/MIT later when starting to work mainly with Python and Django because I thought that this license is a better fit[^license] for the ecosystem. That being said, for a product such as this the GPL is certainly an excellent fit.

[^license]: That's not meant as a criticism in any way!

## Final words?

There are a few things I could write about to make this into a series. I'm putting a few ideas here, not as an announcement, just as a reminder for myself.

- Better time tracking
- Patterns for creating recurring invoices
- Feature switches and configurability
- Coffee time
