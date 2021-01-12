#!/usr/bin/env bash

#set -o errexit

echo "Step1: Install requirements"
pip3 install -r ./requirements.txt

echo "Step2: Run scraping scripts"
cd scrape-scripts
for f in *; do
    python3 $f
done
