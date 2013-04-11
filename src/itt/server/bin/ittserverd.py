#!/usr/bin/python

import argparse

import itt

# TODO - support for HTTP and TFTP
#      - sane config defaults
#      - support for restart and status

def main():
    parser = argparse.ArgumentParser(description='ittserverd')
    parser.add_argument('server_type',
                        choices=['ftp', 'tftp', 'http'],
                        help='The type of server to launch')
    parser.add_argument('action',
                        choices=['start', 'stop', 'restart', 'status'],
                        help='The action to be performed on the server')
    args = parser.parse_args()

    # Select the correct server type with appropriate kwargs.
    server = itt.Config(server=args.server_type)
    daemon = getattr(*server.lookup)(**server.kwargs)

    # Take appropriate action.
    if args.action == "start":
        daemon.start()
    elif args.action == "stop":
        daemon.stop()

if __name__ == "__main__":
    main()
