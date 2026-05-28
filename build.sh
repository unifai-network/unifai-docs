#!/usr/bin/env bash
# Cloudflare Pages (or any CI) build:
#   1. install deps  2. convert the GitBook source -> docs/  3. build the static site -> site/
# Cloudflare Pages settings:
#   Build command:            bash build.sh
#   Build output directory:   site
#   Environment variable:     PYTHON_VERSION = 3.12
set -euo pipefail

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python convert_gitbook.py
python -m mkdocs build --clean

echo "Built site/ ($(find site -type f | wc -l | tr -d ' ') files)"
