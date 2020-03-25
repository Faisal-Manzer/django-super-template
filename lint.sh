#!/usr/bin/env bash

find . -type f \
  -name "*.py" \
  -not -path "./venv/*.*" \
  -not -path "*/migrations/*.py" \
  | xargs pylint \
  --generated-members=objects \
  --disable=C0103,R0903,R0901
