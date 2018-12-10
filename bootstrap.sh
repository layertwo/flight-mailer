#!/bin/bash

mkdir package
cd package/
pip3 install -r ../requirements.txt --target .
cp ../rssr.py lambda_function.py
zip -r9 ../function.zip .
