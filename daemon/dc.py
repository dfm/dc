#!/usr/bin/env python

import os
import subprocess
from urlparse import urlparse
from AppKit import NSWorkspace

def get_current_appname():
    app = NSWorkspace.sharedWorkspace().activeApplication()
    return app["NSApplicationName"]

def get_url_from_chrome():
    cmd = \
"""osascript -e 'tell application "Google Chrome"
    get URL of active tab of first window
end tell'
"""
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    if proc.wait() == 0:
        return urlparse(proc.communicate()[0]).netloc
    return None

def get_filetype_from_vim():
    cmd = \
"""osascript -e 'tell application "MacVim"
    get name of front window
end tell'
"""
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    if proc.wait() == 0:
        try:
            ext = os.path.splitext(proc.communicate()[0].split()[0])[1][1:]
        except:
            return None
        return ext
    return None

if __name__ == '__main__':
    import sys
    import time
    import datetime
    import sqlite3

    # Setup database
    db_fn = os.path.join(*(list(os.path.split(os.path.abspath(__file__))[:-1])+[".dc.db"]))
    db = sqlite3.connect(db_fn)
    cursor = db.cursor()

    if "--info" in sys.argv:
        try:
            N = int(sys.argv[sys.argv.index("--info")+1])
        except:
            N = 10
        print "URLs\n===="
        for d in cursor.execute("""select * from urls order by num desc
                limit ?""", (N,)):
            print d
        print "\nApps\n===="
        for d in cursor.execute("select * from apps"):
            print d
        print "\nUsage\n====="
        for d in cursor.execute("""select * from app_usage order by id desc
                limit ?""", (N,)):
            print d
        print "\nDocument Types\n======== ====="
        for d in cursor.execute("""select * from docs order by id desc
                limit ?""", (N,)):
            print d
        cursor.close()
        sys.exit(0)

    # Create the tables
    cursor.execute("""create table if not exists apps
        (id integer primary key, app text unique)""")
    cursor.execute("""create table if not exists app_usage
        (id integer primary key, app_id integer, year integer, month integer,
        day integer, weekday integer, time real)""")
    cursor.execute("""create table if not exists urls
        (url text primary key, num integer default 0)""")
    cursor.execute("""create table if not exists docs
        (id integer primary key, ext text, year integer, month integer,
        day integer, weekday integer, time real)""")
    db.commit()
    cursor.close()

    try:
        timeout = int(sys.argv[1])
    except IndexError:
        timeout = 60

    while True:
        cursor = db.cursor()
        appname = get_current_appname()
        if appname not in ["loginwindow"]:
            d = datetime.datetime.now()
            ts = (d.hour*60+d.minute)*60+d.second+d.microsecond*1e-6
            date = [d.year, d.month, d.day, d.weekday(), ts]


            cursor.execute("insert or ignore into apps values (null, ?)",
                    (appname,))
            cursor.execute("""insert into app_usage values (null,
                    (select id from apps where app=?), ?,?,?,?,?)""",
                    [appname]+date)

            if appname == "Google Chrome":
                url = get_url_from_chrome()
                if url is not None:
                    cursor.execute("insert or ignore into urls values (?, 0)",
                            (url,))
                    cursor.execute("update urls set num=num+1 where url=?",
                            (url,))
            elif appname == "MacVim":
                ext = get_filetype_from_vim()
                if ext is not None:
                    cursor.execute("insert into docs values (null,?,?,?,?,?)",
                            [ext]+date)

            db.commit()
        cursor.close()
        time.sleep(timeout)

