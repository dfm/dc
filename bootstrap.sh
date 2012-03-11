#!/bin/bash

python daemon/gen_plist.py
launchctl unload -w ~/Library/LaunchAgents/ca.danfm.dc.plist
cp daemon/ca.danfm.dc.plist ~/Library/LaunchAgents/
launchctl load -w ~/Library/LaunchAgents/ca.danfm.dc.plist

(grep "alias gc" ~/.zshrc || echo "alias gc='"`pwd`"/gc.py'" >> ~/.zshrc;source ~/.zshrc)

