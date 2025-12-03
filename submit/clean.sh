#!/usr/bin/env bash

ROOT="${1:-.}"

echo "Cleaning in: $ROOT"

find "$ROOT" -type d -name "__pycache__" -exec rm -rf {} +
find "$ROOT" -type f -name "gmon.out" -delete
find "$ROOT" -type f -name "out.xml" -delete
find "$ROOT" -type f -name "out.midi" -delete

echo "Cleanup complete."