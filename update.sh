#!/bin/bash
python3 setup.py install >/dev/null
python2 setup.py install >/dev/null
git submodule update --init --recursive --remote
cd scapy && git pull origin master && cd ..
python3 run.py && git add -A
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
