#!/bin/bash

clang -o keys/keys keys/keys.m -framework cocoa
python keys/gen_plist.py
launchctl unload -w ~/Library/LaunchAgents/ca.danfm.keys.plist
cp keys/ca.danfm.keys.plist ~/Library/LaunchAgents/
launchctl load -w ~/Library/LaunchAgents/ca.danfm.keys.plist

python daemon/gen_plist.py
launchctl unload -w ~/Library/LaunchAgents/ca.danfm.dc.plist
cp daemon/ca.danfm.dc.plist ~/Library/LaunchAgents/
launchctl load -w ~/Library/LaunchAgents/ca.danfm.dc.plist
