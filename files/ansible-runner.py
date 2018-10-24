#!/usr/bin/env python3
import logging
import logging.handlers
import argparse
import subprocess
import ssh_agent_setup
import time
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

parser = argparse.ArgumentParser()
parser.add_argument("-i","--inventory", help="ansible inventory to use", required=True)
parser.add_argument("-p","--playbook", action='append', help="ansible playbook to run, repeat for multiple plays", required=True)
parser.add_argument("--interval", help="interval in seconds at which to check for new code", default=15)
parser.add_argument("--ssh_id", help="ssh id file to use", default=".ssh/id_rsa")
parser.add_argument("--logdir", help="log dir to watch", default="/srv/git/log")
parser.add_argument("--debug", help="print debugging info to logs")
parser.add_argument("--vault_password_file", help="vault password file", default="~/.vaultpw")
args = parser.parse_args()

logger = logging.getLogger('ansible_runner')
if args.debug:
    logger.setLevel(logging.DEBUG)

# create sysloghandler
sysloghandler = logging.handlers.SysLogHandler(address = '/dev/log')
sysloghandler.setLevel(logging.DEBUG)
# create console handler with a higher log level
consolehandler = logging.StreamHandler()
consolehandler.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
sysloghandler.setFormatter(formatter)
consolehandler.setFormatter(formatter)
# add handlers to the logger
logger.addHandler(consolehandler)
logger.addHandler(sysloghandler)

logger.info ("Starting...")
logger.info ("ssh id: " + args.ssh_id)
logger.info ("logdir: " + args.logdir)
logger.info ("inventory: " + args.inventory)
logger.info ("playbooks: " + args.playbook)
logger.info ("interval: "  +  str(args.interval))

logger.info ("Loading ssh key...")
try:
    ssh_agent_setup.setup()
    ssh_agent_setup.addKey( args.ssh_id )
except Exception:
    logger.exception("Exception adding ssh key, shutting down")
    exit()
else:
    logger.info ("SSH key loaded")

# class to watch args.logdir for changes and run ansible playbook when changes occur
class Watcher:
    DIRECTORY_TO_WATCH = args.logdir

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep( args.interval )
        except:
            self.observer.stop()

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            logger.info ("Received created event - %s." % event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            logger.info ("Received modified event - %s." % event.src_path)
            logger.debug ("ssh id: %s" % args.ssh_id)
            logger.debug ("logdir: %s" % args.logdir)
            logger.debug ("inventory: %s" % args.inventory)
            logger.debug ("playbook: %s" % args.playbook)
            logger.debug ("interval: %s"  %  str(args.interval))
            logger.debug ("Attempting to run ansible-playbook -i %s %s", args.inventory, args.playbook)
            ret = subprocess.call(['ansible-playbook', '-i', args.inventory, '--vault-password-file', args.vault_password_file, args.playbook])
            if ret == 0:
                logger.info ("ansible-playbook return code: %s", ret)
            else:
                logger.error ("ansible-playbook return code: %s", ret)


if __name__ == '__main__':
    w = Watcher()
    w.run()
