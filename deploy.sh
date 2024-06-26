#!/bin/bash

# Rebuild the game
pygbag --build main.py

# Remove old docs directory if it exists
rm -rf docs

# Rename build to docs
mv build docs

# Add all changes to git
git add docs

# Commit changes
git commit -m "Update game build"

# Push to GitHub
git push origin main
