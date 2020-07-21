#!/bin/bash
if [ "$1" == "" ]
then
    echo "Usage: ./read_pr.sh <PR number>"
    exit 1
fi
cd scapy
git pull origin "pull/$1/head" --quiet
git reset --hard origin/master --quiet
echo "OK. You can now run run.sh"
