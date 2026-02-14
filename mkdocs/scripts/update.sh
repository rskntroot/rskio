#!/bin/bash

set -e

repos=("oxpasta" "r53-ddns")
user="rskntroot"
dest_dir="docs/code"

mkdir -p "$dest_dir"

for repo in "${repos[@]}"; do
  url="https://raw.githubusercontent.com/$user/$repo/main/README.md"
  dest_file="$dest_dir/$repo.md"

  echo "Fetching $url -> $dest_file"
  curl -sSfL "$url" -o "$dest_file"
done
