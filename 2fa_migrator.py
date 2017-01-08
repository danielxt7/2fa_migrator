#!/usr/bin/env python
import sys
import subprocess

import qrcode
import sqlite3
import urllib

import click

@click.group()
def cli():
    pass

DB_TYPE_GOOGLE_AUTHENTICATOR = "GA"

# utils
# NOTE: this is just a heuristic that worked well for me (for nice labelling)
def extract_issuer_from_email(email):
    if "@" in email:
        return email.split("@")[1]

    if "-" in email:
        return email.split("-")[0]

    if ":" in email:
        return email.split(":")[0]

# db parsing handlers
def parse_google_authenticator_db(db_path):
    db = sqlite3.connect(db_path)

    for account in db.execute("SELECT * FROM accounts"):
        id, email, secret, _, _, _, issuer = account[:7]

        if issuer is None:
            issuer = extract_issuer_from_email(email)

        label = issuer

        # template: otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example
        line = "otpauth://totp/%s:%s?secret=%s&issuer=%s" % (urllib.quote(label), urllib.quote(email), secret, urllib.quote(issuer))

        yield (id, label, issuer, email, secret, line)


# db pulling handlers
def pull_google_authenticator_db(dest):
    cmdline = "adb pull /data/data/net.singular.authenticator/databases/databases %s" % dest

    print "executing '%s', output:" % cmdline
    pipe = subprocess.Popen(cmdline.split(), stdout=subprocess.PIPE)
    print pipe.stdout.read()
    print
    print "done."


@cli.command(name="generate", help="Generate QR Codes for 2FA database entries")
@click.option("--db", help="Path to database file", required=True)
@click.option("--type", help="database type (default: %s)" % DB_TYPE_GOOGLE_AUTHENTICATOR,
              default=DB_TYPE_GOOGLE_AUTHENTICATOR)
def generate(db, type):
    DB_TYPE_HANDLERS = {
        DB_TYPE_GOOGLE_AUTHENTICATOR: parse_google_authenticator_db
    }

    if type not in DB_TYPE_HANDLERS:
        sys.stderr.write("No handler for db type '%s' for generate! implement it! :)\n" % type)
        sys.exit(1)

    db_type_handler = DB_TYPE_HANDLERS[type]

    for id, label, issuer, email, secret, line in db_type_handler(db):
        filename = "%s.png" % label

        print "writing QR Code for '%s' => %s" % (label, filename)

        qrcode.make(line).save(file(filename, "wb"), "png")

@cli.command(name="pull", help="Pull 2FA database file from your device")
@click.option("--type", help="database type (default: %s)" % DB_TYPE_GOOGLE_AUTHENTICATOR,
              default=DB_TYPE_GOOGLE_AUTHENTICATOR)
@click.option("--dest", help="destination filename (default=db.bin)", default="db.bin")
def pull(type, dest):
    DB_TYPE_HANDLERS = {
        DB_TYPE_GOOGLE_AUTHENTICATOR: pull_google_authenticator_db
    }

    if type not in DB_TYPE_HANDLERS:
        sys.stderr.write("No handler for db type '%s' for pull! implement it! :)\n" % type)
        sys.exit(1)

    db_type_handler = DB_TYPE_HANDLERS[type]

    print "pulling db of type '%s' => %s" % (type, dest)
    db_type_handler(dest)


if __name__ == '__main__':
    cli()
