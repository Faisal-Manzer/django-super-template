#!/usr/bin/env bash

rm -rf venv
rm -rf .git
virtualenv venv
source venv/bin/activate

pip install -r requirements.txt

git init

chmod +x manage.py
chmod +x lint.sh

cat lint.sh >> .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

if [ ! -f secrets.json ]; then
    cp secrets.example.json secrets.json
fi

git add -A
git commit -m "Initial"
