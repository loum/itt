#!/usr/bin/python

import argparse
import os.path

import itt

# TODO - support for HTTP and TFTP
#      - sane config defaults
#      - support for restart and status

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ittserverd')
    parser.add_argument('server_type',
                        choices=['ftp', 'tftp', 'http'],
                        help='The type of server to launch')
    parser.add_argument('action',
                        choices=['start', 'stop', 'restart', 'status'],
                        help='The action to be performed on the server')
    args = parser.parse_args()

    # Construct the PID file name based on server type.
    this_script = os.path.basename(__file__)
    pid_file = '/tmp/%s.%s.pid' % (this_script, args.server_type)

    daemon = itt.FtpServer(root='/tmp', pidfile=pid_file)

    if args.action == "start":
        daemon.start()
    elif args.action == "stop":
        daemon.stop()
