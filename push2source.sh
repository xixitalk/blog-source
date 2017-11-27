#!/bin/bash

# Add changes to git.
git add  config.toml
git add -A content/post/*.md 
git add -A static

# Commit changes.
msg="blog source push `date`"
if [ $# -eq 1 ]
  then msg="$1"
fi
git commit -m "$msg"

# Push source and build repos.
git push origin master

