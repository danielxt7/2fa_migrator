#!/usr/bin/env python

import qrcode
import sqlite3
import urllib

db = sqlite3.connect("/tmp/db.sqlite")

for account in db.execute("SELECT * FROM accounts"):
    id, email, secret, _, _, _, issuer = account[:7]

    label = email

    if issuer is None:
        if "@" in email:
            label = issuer = email.split("@")[1]
        elif "-" in email:
            label = issuer = email.split("-")[0]
        elif ":" in email:
            label = issuer = email.split(":")[0]

    email = urllib.quote(email)
    issuer = urllib.quote(issuer)
    label = urllib.quote(label)

    # template: otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example
    line = "otpauth://totp/%s:%s?secret=%s&issuer=%s" % (label, email, secret, issuer)
    print line

    qrcode.make(line).save(file("%s.png" % id, "wb"), "png")
