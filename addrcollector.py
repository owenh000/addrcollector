#!/usr/bin/python3
# Depends: python3-xdg, python3-docopt
"""addrcollector: Collect email addresses for later retrieval, or
search the database of previously collected addresses.

Usage:
  addrcollector.py --add ADDRESS [NAME]
  addrcollector.py --import
  addrcollector.py --search WORD...
  addrcollector.py --help

Options, arguments, and commands:
  -a --add      Manually add an address.
  ADDRESS       Email address to add to database.
  NAME          Name to associate with email address (optional).
  -i --import   Import addresses from headers of one message via standard input.
  -s --search   Search database for addresses; multiple keys are ORed.
  WORD          Search key.
  -h --help     Usage help.

"""

import email.parser
from email.utils import getaddresses
import os.path
import re
import sqlite3
import sys
import time
import warnings

from docopt import docopt
import xdg.BaseDirectory

class Database:
    """Manage the sqlite3 addrcollector database."""

    def __init__(self):
        """
        Create path/database if necessary, connect, 5% chance of
        cleaning database *unless* opening only to search, and save
        the connection.
        """
        self.db_path = os.path.join(xdg.BaseDirectory.save_data_path
                                    ('addrcollector'), 'database.db')
        if os.path.exists(self.db_path): new=False
        else: new=True
        self.conn = sqlite3.connect(self.db_path)
        if new==True:
            self.conn.execute('''CREATE TABLE address
                                  (name TEXT,
                                   address TEXT PRIMARY KEY,
                                   time INTEGER)''')
        # Comment out the following to disable automatic database purging
        #if not arguments['--search'] and random.random() < 0.05:
        #    self.conn.execute('DELETE FROM address WHERE time < ?',
        #                      (int(time.time()) - 1262277050,)) # 40 years

    def add_address(self, name, address):
        """
        Add an entry to the database.  If it already exists, then (1)
        update the time and (2) if the new name is longer, then update
        the name.
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
        """
        Search for addresses with any of arguments in strings, which
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
    arguments = docopt(__doc__)
    db = Database()
    if arguments['--add']:
        db.add_address(name=arguments['NAME'], address=arguments['ADDRESS'])
    elif arguments['--import']:
        for addr in parse_email(sys.stdin.read()):
            db.add_address(name=addr[0], address=addr[1])
    elif arguments['--search']:
        for result_item in db.search(arguments['WORD']):
            print('{} {:<30} {}'.format(*result_item))
    db.close()

if __name__ == '__main__':
    main()
