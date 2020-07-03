=============
addrcollector
=============

A Python application for collecting email addresses from email messages

-----
About
-----

*addrcollector* collects email addresses from email messages. This is
similar to Thunderbird's "Collected Addresses" feature and
corresponding functionality in other software. In the case of
addrcollector, however, email messages are read from standard input,
or manually on the command line, and the email address database can be
queried by keyword.

It is possible for addrcollector to be integrated with a mail delivery
system like Procmail or Maildrop to collect addresses from all
messages, or with mail clients like Mutt or Alpine to collect
addresses selectively.

Dates and display names are also collected. If an address is seen more
than once, then (1) the date is updated and (2) the display name is
updated if the new one is longer than the old one.

.. code:: console

   $ addrcollector --help
   addrcollector: Collect email addresses for later retrieval, or
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

------------
Dependencies
------------

addrcollector depends on the following Python packages not in the
standard library:

- docopt
- xdg

---------------------
Copyright and License
---------------------

Copyright 2020 Owen T. Heisler. Creative Commons Zero v1.0 Universal
(CC0 1.0).

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

This source code may be used, modified, and/or redistributed according
to the terms of the Creative Commons Zero 1.0 Universal (CC0 1.0)
license. You should have received a copy of this license along with
this program (see `LICENSE`). If not, see
<https://creativecommons.org/publicdomain/zero/1.0/>.
