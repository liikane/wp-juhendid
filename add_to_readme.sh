#!/bin/bash
cat README_HEADER.md > README.md
echo "" >> README.md
echo "### Failid:" >> README.md
for f in *.md *.html; do
  if [[ "$f" != "README.md" && -f "$f" ]]; then
    echo "- [$f]($f)" >> README.md
  fi
done
