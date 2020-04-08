#!/bin/bash
git submodule update --init --recursive --remote
python2 run.py && git add -A
git status
read -p "Publish? [n]: " publish
if [ "$publish" == "y" ] || [ "$publish" == "yes" ]
then
  git commit -m "New automated update"
  git push
fi
