Title: Weeknotes (2023 week 16)
Date: 2023-04-21
Categories: Politik, Django, Programming, Weeknotes

# Weeknotes (2023 week 16)

## Experiments with Stable Diffusion

A friend and myself threw a few scripts together to automatically finetune a Stable Diffusion model using images downloaded from Google Image search. It's terrifying how easy and fast generating fake news including photorealistic images can be and will be already. And seeing how fast those models improve it's just a matter of time until we can trust photos even less than now. Manipulating images has been possible for a long time of course, but it hasn't been a "commodity" until now.

I definitely also see upsides in the new machine learning technologies but I fear that there's a real danger to trust, and in extension to democracy.

This technology and what we did will be a part of an upcoming [SRF Kulturplatz](https://www.srf.ch/play/tv/sendung/kulturplatz?id=d70e9bb9-0cee-46b6-8d87-7cbd8317a9c7) broadcast, or so I hope. It's high time that the public knows what's possible. It's about **media literacy** really.

I'm not that pessimistic though. I just hope that this time the thoughtfulness will prevail over pure profit seeking. (Did I really write that.)

## [django-ckeditor](https://github.com/django-ckeditor/django-ckeditor)

Many people are noticing that the CKEditor 4 integration for Django doesn't work that well when using the dark color scheme of the Django admin panel. That's not surprising. What does surprise me is the number of reports and the total absence of pull requests. Subjectively, most other packages I help maintain have a comfortable ratio of issues and pull requests.

I'm not complaining and people aren't complaining, almost everyone is nice and tries to be helpful. Since I'm not a heavy user of django-ckeditor anymore I don't really find the motivation to fix this issue myself since it's not all that enjoyable work to me. I would just hope that [after all this time](https://github.com/django-ckeditor/django-ckeditor/issues/670) someone would finally come and do the necessary work -- if they cared enough.

## django-mptt

I have marked [django-mptt](https://github.com/django-mptt/django-mptt) as unmaintained two years ago. I'm still looking at pull requests from time to time but without feeling an obligation to do so and without feeling bad when I miss something.

I wonder if there are still many people out there who still depend on this library and if any of them would be willing to pick up the maintenance? On the off chance that someone is out there who has the time, ability and motivation and just didn't know that django-mptt could use some love: Here's your invite!
