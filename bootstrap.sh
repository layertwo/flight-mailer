#!/bin/bash

mkdir package
cd package/
pip3 install -r ../requirements.txt --target .
cp ../rssr.py lambda_function.py
cp ../template.html ../feeds.jsonl .
zip -r9 ../function.zip .
