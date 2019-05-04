#!/bin/bash

# Remove old artifacts
rm -rf packages
rm ../smart-form-lambda-funcs.zip

mkdir packages
pip3 install -r requirements.txt -t packages/
chmod -R 755 .

cd packages
zip -r ../../smart-form-lambda-funcs.zip .
cd "$OLDPWD"
zip -g ../smart-form-lambda-funcs.zip get_recommendations_func.py
zip -g ../smart-form-lambda-funcs.zip gen_rules_func.py
