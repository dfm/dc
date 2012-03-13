#!/usr/bin/env python

__all__ = ["send_email"]

from db import db

def send_email():
    cursor = db.cursor()
    apps = dict([d for d in cursor.execute("select * from apps")])
    usage = dict([(k, 0) for k in apps])
    for d in cursor.execute("select * from app_usage order by id desc"):
        usage[d[1]] += 1
    for k in apps:
        print apps[k], usage[k]
    cursor.close()

if __name__ == '__main__':
    send_email()

