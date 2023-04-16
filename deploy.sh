#!/bin/sh
git push -u origin main
venv/bin/python generate.py
rsync -avzhP --delete out/ www-data@feinheit06.nine.ch:406.ch/htdocs/
