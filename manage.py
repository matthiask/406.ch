#!/usr/bin/env python
import speckenv
import os
import sys

if __name__ == "__main__":
    speckenv.read_speckenv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mkweb.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
