#!/bin/bash
trap "exit" INT TERM
trap "kill 0" EXIT

export PYTHONWARNINGS=always
export PYTHONUNBUFFERED=yes
set -ex

(
  # Start the HTTP server
  mkdir -p htdocs && cd htdocs && uv run python -m http.server 8001
) &
(
  # Run entr -d (exits when new files are added) in a loop while ignoring everything in htdocs and git
  while true; do
    find . -not -path './htdocs/*' -not -path './.git/*' -type f \
        | entr -d uv run python -Wd -c 'import generate as g; g.main(only_published=False, base_url="http://localhost:8001")'
  done
) &

uv run python -m webbrowser "http://localhost:8001"

for job in $(jobs -p); do wait $job; done
