#!/bin/bash

python gen_plist.py
launchctl unload -w ~/Library/LaunchAgents/ca.danfm.dc.plist
cp ca.danfm.dc.plist ~/Library/LaunchAgents/
launchctl load -w ~/Library/LaunchAgents/ca.danfm.dc.plist

