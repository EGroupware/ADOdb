#!/usr/bin/env -S python3 -u
"""
ADOdb announcements script.

Posts release announcements to Gitter

This file is part of ADOdb, a Database Abstraction Layer library for PHP.

@package ADOdb
@link https://adodb.org Project's web site and documentation
@link https://github.com/ADOdb/ADOdb Source code and issue tracker

The ADOdb Library is dual-licensed, released under both the BSD 3-Clause
and the GNU Lesser General Public Licence (LGPL) v2.1 or, at your option,
any later version. This means you can use it in proprietary products.
See the LICENSE.md file distributed with this source code for details.
@license BSD-3-Clause
@license LGPL-2.1-or-later

@copyright 2022 Damien Regad, Mark Newnham and the ADOdb community
@author Damien Regad
"""

import argparse
from pathlib import Path

from git import Repo  # https://gitpython.readthedocs.io
from adodbutil import env, Gitter


def process_command_line():
    """
    Parse command-line options
    :return: Namespace
    """
    # Get most recent Git tag
    repo = Repo(path=Path(__file__).parents[1])
    tags = sorted(repo.tags, key=lambda t: t.tag.tagged_date)
    latest_tag = str(tags[-1])

    parser = argparse.ArgumentParser(
        description="Post ADOdb release announcement messages to Gitter."
    )
    parser.add_argument('version',
                        nargs='?',
                        default=latest_tag,
                        help="Version number to announce; if not specified, "
                             "the latest tag will be used.")
    parser.add_argument('-m', '--message',
                        help="Additional text to add to announcement message")

    return parser.parse_args()


def post_gitter(message):
    print("Posting to Gitter... ", end='')
    gitter = Gitter(env.gitter_token, env.gitter_room)
    message_id = gitter.post('# ' + message)
    print("Message posted successfully\n"
          "https://gitter.im/{}?at={}"
          .format(env.gitter_room, message_id))
    print()


def main():
    args = process_command_line()

    # Build announcement message
    message = """ADOdb Version {0} released{1}
See changelog https://github.com/ADOdb/ADOdb/blob/v{0}/docs/changelog.md""" \
        .format(args.version.lstrip('v'),
                "\n" + args.message.rstrip(".") + "." if args.message else "")

    # Get confirmation
    print("Review announcement message")
    print("-" * 27)
    print(message)
    print("-" * 27)
    reply = input("Proceed with posting ? ")
    if not reply.casefold() == 'y':
        print("Aborting")
        exit(1)

    post_gitter(message)


if __name__ == "__main__":
    main()
