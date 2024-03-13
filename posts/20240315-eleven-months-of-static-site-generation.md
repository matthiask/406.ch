Title: Eleven months of static site generation
Date: 2024-03-15
Categories: Programming

Almost eleven months have gone by since I [last wrote](https://406.ch/writing/the-insides-of-my-static-site-generator/) about the [static site generator script](https://github.com/matthiask/406.ch/blob/main/generate.py) I'm using for this website.

## What has changed in the meantime?

- The build script is 40 lines shorter.
- Code snippets are now highlighted using pygments.
- The script now not only reports how many files have been written but also the
  categories and their post count.
- The script now supports a folder with static assets so that images etc. do
  not have to be hotlinked from elsewhere. Hotlinking images hosted in GitHub
  issues doesn't work anymore it seems.
- The execution time isn't reported anymore.
- The script now supports scheduled publishing, mainly by leveraging GitHub
  action's scheduling support.


## Has it been worth it?

The general advice seems to not write your own static site generator because
you'll spend time tweaking the generator instead of actually writing posts.
This definitely doesn't have to be the case. Sometimes it's good to hack on a
small projects just for the joy of it. I certainly enjoy the fact that my code
(arguably 🙃) does something useful each time I publish a new post.
