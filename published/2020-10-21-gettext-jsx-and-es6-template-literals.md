Title: gettext, JSX and ES6 template literals
Slug: gettext-jsx-and-es6-template-literals
Date: 2020-10-21
Categories: Django, Programming

# gettext, JSX and ES6 template literals

I really like using [gettext](https://www.gnu.org/software/gettext/) to translate hardcoded strings into other languages. [Django's translations functionality](https://docs.djangoproject.com/en/3.1/topics/i18n/translation/) relies on it as well.

Unfortunately, the xgettext executable which is responsible to collect translatable strings in your code has a bug where it just stops processing files when encountering ES6 template literals inside JSX tags. Support for ES6 template literals was added [earlier this year](https://savannah.gnu.org/bugs/?50920) but combining those literals with JSX [still doesn't work](https://savannah.gnu.org/bugs/?58407).

I wrote a small Python script to extract `*gettext` calls from JavaScript files; the current version is [here](https://github.com/matthiask/workbench/blob/main/extract_gettext.py). The idea is to find all JavaScript files using `git ls-files "*.js"`, using a regular expression to find `*gettext` calls and write the output to a place where Django's `./manage.py makemessages` finds it.

I'm certain the code will break too with strange error messages in the near future but it seems to work well, for the moment.

Here's the current version of the code (hopefully) for your enjoyment:

    #!/usr/bin/env python3

    import re
    import subprocess


    def js_files():
        res = subprocess.run(
            ["git", "ls-files", "*js", "*mjs"],
            capture_output=True,
            encoding="utf-8",
        )
        return res.stdout.splitlines()


    def gettext_calls(file):
        with open(file, encoding="utf-8") as f:
            return [
                f"{match[0]}({match[1]})"
                for match in re.findall(
                    r"""\b(\w*gettext)\(\s*((['"]).+?\3)\s*\)""",
                    f.read(),
                )
            ]


    if __name__ == "__main__":
        calls = []
        for file in js_files():
            calls.extend(gettext_calls(file))
        print("\n".join(sorted(set(calls))))
