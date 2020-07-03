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

--------------------
Installing from PyPI
--------------------

addrcollector is published on PyPI and can be installed with pip.

1. Install the addrcollector package.

   .. code:: console

      $ pip3 install addrcollector

   This should provide a ``~/.local/bin/addrcollector`` script that you
   can execute.

2. If that path is included in your `PATH` environment variable, you
   can run the ``addrcollector`` command without typing the entire
   path., To set up this, if it hasn't been done already, add the
   following code in your ``~/.bash_profile`` (it may be
   ``~/.profile`` for a shell other than Bash):

   .. code:: bash

      if [ -d "$HOME/.local/bin" ] ; then
          PATH="$HOME/.local/bin:$PATH"
      fi

-----------------------
Running from repository
-----------------------

If you have cloned the repository, you can run addrcollector from it
directly.

1. Install Poetry:

   .. code:: console

      $ pip3 install poetry

2. With the addrcollector repository root as your current directory,
   use Poetry to install the dependencies:

   .. code:: console

      $ poetry install

3. Now that the dependencies have been installed, use Poetry to run
   addrcollector:

   .. code:: console

      $ poetry run addrcollector

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
