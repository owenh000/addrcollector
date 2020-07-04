#!/usr/bin/python3
"""Collects email addresses in a database or searches the database.

Addresses can be added manually or imported from a message passed on
standard input. Dates and display names are also collected. If an
address is seen more than once, then (1) the date is updated and (2)
the display name is updated if the new one is longer than the old
one. Once addresses have been added, the database can be searched with
one or more keywords.

Usage examples:
  addrcollector add jon@mykolab.com "Jon Smith"
  addrcollector import < mymail.msg
  addrcollector search jon
"""

import argparse
import email.parser
from email.utils import getaddresses
import os
from pathlib import Path
import re
import sqlite3
import sys
import time
import warnings


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__)
    subp = parser.add_subparsers(title='actions',
                                 dest='action', required=True)
    addp = subp.add_parser('add', aliases=['a'],
                           help='Manually add an address to the database')
    addp.add_argument('address', help='Email address')
    addp.add_argument('name', help='Display name (optional)', nargs='?')
    impp = subp.add_parser('import', aliases=['i'],
                    help='Import addresses from a message on standard input')
    srchp = subp.add_parser('search',  aliases=['s'],
                            help='Search the database for addresses')
    srchp.add_argument('word', nargs='+',
                help='Keyword to search for (may be specified more than once)')
    return parser.parse_args()


class Database:
    """Manage the sqlite3 addrcollector database."""

    def __init__(self):
        """Create database if necessary, connect, save the connection"""
        envvar = os.environ.get('XDG_DATA_HOME')
        if envvar:
            data_dir = Path(envvar)
        else:
            data_dir = Path(os.path.expandvars('$HOME'), '.local', 'share')
        self.db_path = os.path.join(data_dir, 'addrcollector', 'database.db')
        self.conn = sqlite3.connect(self.db_path)
        if not os.path.exists(self.db_path):
            # New database
            self.conn.execute('''CREATE TABLE address
                                  (name TEXT,
                                   address TEXT PRIMARY KEY,
                                   time INTEGER)''')
        # This can be used for 5% chance of purging out any records that are
        # older than 10 years:
        #if not arguments['--search'] and random.random() < 0.05:
        #    self.conn.execute('DELETE FROM address WHERE time < ?',
        #                      (int(time.time()) - 315569260,))

    def add_address(self, name, address):
        """Add an entry to the database.

        If it already exists, then (1) update the time and (2) if the
        new name is longer, then update the name.

        """
        address=address.lower()
        if not re.match(r'[^@]+@[^@]+\.[^@]+', address):
            raise Exception('The provided address does not appear to be valid.')
        prev = self.conn.execute('SELECT * FROM address WHERE address==?',
                                     (address,)).fetchone()
        if name == None:
            name=''
        if prev == None:
            # not pre-existing, insert record
            self.conn.execute('INSERT INTO address VALUES (?,?,?)',
                              (name, address, int(time.time())))
        elif len(name) >= len(prev[0]):
            # new name is same or greater length, update name, time
            self.conn.execute('''UPDATE address
                                 SET name=?, time=? WHERE address=?''',
                              (name, int(time.time()), address))
        else:
            # new name is shorter length, only update time
            self.conn.execute('UPDATE address SET time=? WHERE address=?',
                              (int(time.time()), address))

    def search(self, strings):
        """Search for addresses.

        Search in the database for any of arguments in strings, which
        is a list of queries.

        """
        search_str = ' OR '.join(['address||name LIKE ?' for string in strings])
        search_params = tuple('%{0}%'.format(string) for string in strings)
        query = self.conn.execute(
            ' '.join(['SELECT * FROM address WHERE', search_str,
                      'ORDER BY time ASC']),
            search_params)
        for result in query:
            yield(time.strftime('%Y-%m-%d', time.localtime(result[2])),
                  result[1], result[0])

    def close(self):
        """Close the database."""
        self.conn.commit()
        self.conn.close()


def parse_email(src):
    """Collect addresses from headers of email message."""
    parser = email.parser.HeaderParser()
    headers = parser.parsestr(src)
    tos = headers.get_all('to', [])
    ccs = headers.get_all('cc', [])
    resent_tos = headers.get_all('resent-to', [])
    resent_ccs = headers.get_all('resent-cc', [])
    senders = headers.get_all('sender', [])
    froms = headers.get_all('from', [])
    addrs = getaddresses(tos + ccs + resent_tos + resent_ccs + senders + froms)
    for addr in addrs:
        yield(addr)


def main():
    args = parse_args()
    db = Database()
    if args.action in ['add', 'a']:
        db.add_address(name=args.name, address=args.address)
    elif args.action in ['import', 'i']:
        for addr in parse_email(sys.stdin.read()):
            db.add_address(name=addr[0], address=addr[1])
    else: #args.action in ['search', 's']
        for result_item in db.search(args.word):
            print('{} {:<30} {}'.format(*result_item))
    db.close()


if __name__ == '__main__':
    main()
