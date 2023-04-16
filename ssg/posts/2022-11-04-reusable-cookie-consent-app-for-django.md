Title: Reusable cookie consent app for Django
Slug: reusable-cookie-consent-app-for-django
Status: published
Date: 2022-11-04
Categories: Django, Programming
Type: markdown

# Reusable cookie consent app for Django

[We at Feinheit](https://feinheit.ch/) have been working on a cookie consent app for some time.

![The cookie banner](https://raw.githubusercontent.com/feinheit/feincms3-cookiecontrol/main/docs/banner.png)

## Why and what?

There are many many solutions in this problem space already. We have used several scripts in the past. Some are simple banners or popups which only inform users that cookies are being used. It is our view and belief that this isn't sufficient to fulfil the legal obligations imposed by the GDPR and other comparable legislations.

We wanted a way to ask for consent and only embed any third party scripts after the consent has been given, not use some other tool which only comes into action after e.g. the Google Analytics scripts already have been loaded.

Accepting only essential cookies is made very annoying by some cookie banners. They drown users in options and nudge (or maybe coerce) them towards accepting _all_ cookies. The banner buttons are inspired (stealed) from Twitter, we think it's nice to offer as little options as possible.

## Embedding third party content

Also, we wanted to integrate a solution for embedding content from third party sites (e.g. Vimeo, Mailchimp and friends) where consent was asked as well when users only accept essential (first party) cookies:

![Consciously embedding a YouTube video](https://raw.githubusercontent.com/feinheit/feincms3-cookiecontrol/main/docs/embed.png)

That's why we set out to build a simple solution doing all that. As always it's released as Open Source since we believe that giving back is the right thing to do (tm) _and_ it helps with [managing complexity in our projects](https://406.ch/writing/managing-complexity-and-technical-debt-by-releasing-open-source-software/).

## feincms3-cookiecontrol

The name of the project is [feincms3-cookiecontrol](https://github.com/feinheit/feincms3-cookiecontrol). It has reached the 1.0 version and we're committed to backwards compatibility. The conscious embedding functionality depends on [feincms3's embedding module](https://feincms3.readthedocs.io/en/latest/ref/embedding.html), everything else also works with Django only.
