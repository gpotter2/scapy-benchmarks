#!/bin/bash
python2 setup.py install
git submodule update --init --recursive --remote
python2 run.py && git add -A
if [ "$?" == "1" ]
then
  exit 1
fi
git status
read -p "Publish? [n]: " publish
if [ "$publish" == "y" ] || [ "$publish" == "yes" ]
then
  git commit -m "New automated update"
  git push
fi
