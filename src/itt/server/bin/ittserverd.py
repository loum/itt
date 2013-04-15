#!/usr/bin/python

import argparse
import sys

import itt

# TODO - support for status check
#      - support for "all" server action

def main():
    parser = argparse.ArgumentParser(description='ittserverd')
    parser.add_argument('server_type',
                        choices=['ftp', 'tftp', 'http'],
                        help='The type of server to control')
    parser.add_argument('action',
                        choices=['start', 'stop', 'restart', 'status'],
                        help='The action to be performed on the server')
    args = parser.parse_args()

    # Select the correct server type with appropriate kwargs.
    server = itt.Config(server=args.server_type)
    try:
        daemon = getattr(*server.lookup)(**server.kwargs)
    except KeyError:
        err_msg = ('Server "%s" config section does not exist.' %
                   args.server_type)
        sys.stderr.write('ERROR: %s' % err_msg)
        sys.exit(1)

    # Take appropriate action.
    if args.action == "start":
        daemon.start()
    elif args.action == "stop":
        daemon.stop()
    elif args.action == "restart":
        daemon.restart()

if __name__ == "__main__":
    main()
