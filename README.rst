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

For example, to add an address manually (the display name is optional):

.. code:: console

   $ addrcollector add jon@example.com "Jon Smith"
   $ addrcollector add sven@example.com

To import addresses from a message passed on standard input:

.. code:: console

   $ addrcollector import < mymail.msg

To search for addresses using keywords (multiple keywords may be
given and are ORed):

.. code:: console

   $ addrcollector search jon sven
   2020-07-03 jon@example.com                Jon Smith
   2020-07-03 sven@example.com

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
   path. To set this up (if it hasn't been done already), add the
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

--------
Sponsors
--------

Thank you to an anonymous sponsor for supporting my work on this and
other projects! ✨

------------
Contributing
------------

If you interested in contributing to this project, thank you!

- Share this project with someone else who may be interested
- Contribute a fix for a currently open
  [issue](https://github.com/owenh000/addrcollector/issues) (if any)
  using a GitHub pull request (please discuss before working on any
  large changes)
- Open a new issue for a problem you've discovered or a possible
  enhancement
- Sponsor my work through `GitHub Sponsors
  <https://github.com/owenh000>`_ (see also `owenh.net/support
  <https://owenh.net/support>`_)

Thank you for your interest!

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
