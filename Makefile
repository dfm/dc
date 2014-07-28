PLIST = ${HOME}/Library/LaunchAgents/io.dfm.keys.plist
EXEC := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))bin/keys
DB = /Library/Application\ Support/com.apple.TCC/TCC.db

default: access

keys: src/keys.m
	clang -o ${EXEC} src/keys.m -framework cocoa

plist: plist.py data/template.plist
	python plist.py ${PLIST}

install: clean keys plist
	launchctl load ${HOME}/Library/LaunchAgents/io.dfm.keys.plist

access: install
	sudo sqlite3 ${DB} "INSERT INTO access VALUES('kTCCServiceAccessibility','${EXEC}',1,1,1,NULL);"

clean:
	rm -rf ${EXEC}
	- launchctl unload ${HOME}/Library/LaunchAgents/io.dfm.keys.plist
	sudo sqlite3 ${DB} "DELETE FROM access WHERE client='${EXEC}';"

.PHONY: clean
