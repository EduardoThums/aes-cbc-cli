#!/bin/bash

rm -rf venv
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt -q 2>/dev/null
deactivate
rm -rf bundle
mkdir bundle
mkdir bundle/src
cp -R ./venv/lib/python3.7/site-packages/* bundle
cp cli.py bundle
cd bundle
zip ../bundle.zip -r . -q
cd ..
rm -rf bundle
