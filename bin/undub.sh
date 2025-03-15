#!/bin/sh

# Remove all duplicates
awk '!seen[$0]++' "$@"
