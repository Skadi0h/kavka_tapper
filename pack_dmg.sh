#!/bin/sh
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -r dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "dist/kavka_tapper.app" dist/dmg
# If the DMG already exists, delete it.
test -f "dist/kavka_tapper.dmg" && rm "dist/kavka_tapper.dmg"
create-dmg \
  --volname "kavka_tapper" \
  --volicon "kavka.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "kavka_tapper.app" 175 120 \
  --hide-extension "kavka_tapper.app" \
  --app-drop-link 425 120 \
  "dist/kavka_tapper.dmg" \
  "dist/dmg/"