Title: Weeknotes (2023 week 8 and 9)
Slug: weeknotes-2023-week-8-and-9
Date: 2023-03-03
Categories: Django, Programming, Weeknotes
Type: markdown

# Weeknotes (2023 week 8 and 9)

Last week was a short work week. We spent a few nights in the mountains. Not much snow though. Enough for some skiing and sledging.

This work week was ... not normal. Many meetings, not enough time to work on projects. That shortens these week notes a lot.

## Django Software Foundation membership

I found out through Tim that I have been [approved as an individual member of the Django Software Foundation](https://www.djangoproject.com/foundation/minutes/2023/jan/12/dsf-board-monthly-meeting/). I'm honored and hope that this will be another way where I can give something back. It also feels good to be seen.

I didn't even know that the Foundation's [meeting minutes](https://www.djangoproject.com/foundation/minutes/) were public. I still use RSS and can wholeheartedly recommend [The Old Reader](https://theoldreader.com/) (no affiliation) and so I thought I'd try adding a RSS feed of meeting minutes to the website. [The pull request is still being reviewed.](https://github.com/django/djangoproject.com/pull/1316) at the time of writing.

## feincms3-forms documentation

I worked on the [feincms3-forms](https://github.com/matthiask/feincms3-forms) README a bit. The README hopefully clarifies the purpose and the components of the app a bit.

> This is an extremely flexible forms builder for the Django admin interface.

## Migrating from Bitbucket to GitHub

I have been a long time Bitbucket user since GitHub used a pricing where many private repositories were very expensive and Bitbucket only charged a fee per user. This has changed long ago though. I wanted to consolidate the tools used at $work and have therefore taken the time to move all private repositores to GitHub. Determining the list of repositories in a Bitbucket Workspace was surprisingly annoying but I got there in the end with an app-specific password and curl.

Next, I converted the JSON into a list of Git/SSH cloning URLs:

    import json, sys

    d = json.loads(sys.stdin.read())
    print(
        "\n".join(
            next(link["href"] for link in rec["links"]["clone"] if link["name"] == "ssh")
            for rec in d["values"]
        )
    )

I used it as (I had to repeat the first command for every 100 repos):

    python3 filter.py < repos.json >> clone.txt
    for url in $(cat clone.txt); do (cd mirror; git clone --mirror $url) ; done

Then, I wrote another Python script to create the repositores and upload them all:

    import sys
    from subprocess import run

    for repo in sys.argv[1:]:
        run(f"gh repo create --private feinheit-archive/{repo[:-4]}", shell=True, check=True)
        run(f"cd {repo} && git push git@github.com:feinheit-archive/{repo[:-4]}.git --all", shell=True, check=True)
        run(f"rm -rf {repo}", shell=True, check=True)

And ran ist as:

    cd mirror
    python3 ../upload.py *

Funnily enough I learned that GitHub ratelimits repository creation. So I had to wait an hour after several dozen repos and start the command again afterwards. Of course the code wasn't written defensively at first and deleted repos which weren't uploaded yet so I had to work out the set of repos I have to re-download from Bitbucket... I think it's a bit surprising that `subprocess.run` doesn't raise an exception by default when a command fails. `check=True` should definitely be the default.

I'm not posting the code because I'm proud but because I'm not. Throwing such stuff together with Python feels great, and using `subprocess.run(..., shell=True)` is more fun than writing bash scripts with `sed` etc.

## Use Frontend frameworks to kickstart your site and to drag you down later

A longer blog post is in the making as I'm trying to formulate my thoughts on this.

Frontend frameworks are a great help in getting a product out of the door quickly. But tools and needs evolve. Backwards incompatible versions[^semver] of those Frameworks are published. And then it happens: Too many things break at once and you have to pick up the pieces. What has been an advantage in the beginning drags you down, because now you have to maintain not just your own code but also everything you used from $framework.

I wish I had been (even 😂) more cautious when selecting tools for potentially long running projects.

[^semver]: Sometimes stuff breaks even when updating patch versions.
