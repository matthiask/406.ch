#!/bin/bash
trap "exit" INT TERM
trap "kill 0" EXIT

export PYTHONWARNINGS=always
export PYTHONUNBUFFERED=yes

set -ex
(mkdir -p htdocs && cd htdocs && npx serve) &
(git ls-files | entr uv run python -Wd -c 'import generate as g; g.main(only_published=False, base_url="http://localhost:3000")') &

for job in $(jobs -p); do wait $job; done
