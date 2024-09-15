#!/bin/bash
trap "exit" INT TERM
trap "kill 0" EXIT

export PYTHONWARNINGS=always
export PYTHONUNBUFFERED=yes

set -ex
(cd htdocs; python3 -m http.server 8001) &
(git ls-files | entr uv run python -Wd -c 'import generate as g; g.main(only_published=False)') &

for job in $(jobs -p); do wait $job; done
