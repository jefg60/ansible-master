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
from os.path import expanduser
import glob

home = expanduser("~")
__version__ = "0.2"

parser = argparse.ArgumentParser()
parser.add_argument("-v", "-V", "--version", action="version", version=__version__)
parser.add_argument("--interval", help="interval in seconds at which to check for new code", default=15)
parser.add_argument("--ssh_id", help="ssh id file to use", default=home + "/.ssh/id_rsa")
parser.add_argument("--logdir", help="log dir to watch", default="/srv/git/log")
parser.add_argument("--debug", help="print debugging info to logs")
parser.add_argument("--vault_password_file", help="vault password file", default=home + "/.vaultpw")
parser.add_argument("--syntax_check_dir", help="Optional directory to search for *.yml and *.yaml files to syntax check when changes are detected")

playbookgroup = parser.add_mutually_exclusive_group(required=True)
playbookgroup.add_argument("-p","--playbook", action='append', help="a single ansible playbook to run")
playbookgroup.add_argument("--playbooks", nargs='*', help="space separated list of ansible playbooks to run. Overrides --playbook")

inventorygroup = parser.add_mutually_exclusive_group(required=True)
inventorygroup.add_argument("-i","--inventory", help="a single ansible inventory to use")
inventorygroup.add_argument("--inventories", help="space separated list of ansible inventories to syntax check against. Overrides --inventory. The first inventory file will be the one that playbooks are run against if syntax checks pass")

args = parser.parse_args()

if args.syntax_check_dir is not None:
    yamlfiles = glob.glob(args.syntax_check_dir + '/*.yaml')
    ymlfiles = glob.glob(args.syntax_check_dir + '/*.yml')
    yamlfiles = yamlfiles + ymlfiles

if args.playbook is not None:
    playstorun = args.playbook
if args.playbooks is not None:
    playstorun = args.playbooks

if args.inventory is not None:
    workinginventorylist = [ args.inventory ]
    maininventory = args.inventory
if args.inventories is not None:
    workinginventorylist = args.inventories
    maininventory = args.inventories[0]

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
logger.info ("inventorylist: " + " ".join(workinginventorylist))
logger.info ("playbooks: " + " ".join(playstorun))
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

def checkplaybooks(listofplaybooks,listofinventories):
    badSyntaxPlaybooks = []
    badSyntaxInventories = []
    for p in listofplaybooks:
        for i in listofinventories:
            logger.debug ("Syntax Checking ansible playbook %s against inventory %s", p, i)
            ret = subprocess.call(['ansible-playbook', '-i', i, '--vault-password-file', args.vault_password_file, p, '--syntax-check'])
            if ret == 0:
                logger.info ("ansible-playbook syntax check return code: %s", ret)
            else:
                logger.error ("ansible-playbook syntax check return code: %s", ret)
                badSyntaxPlaybooks.append(p)
                badSyntaxInventories.append(i)
    return badSyntaxPlaybooks + badSyntaxInventories

def checkeverything():
    problemlist = checkplaybooks(yamlfiles,workinginventorylist)
    return problemlist

def runplaybooks(listofplaybooks):
    for p in listofplaybooks:
        logger.debug ("Attempting to run ansible-playbook -i %s %s", inventory, p)
        ret = subprocess.call(['ansible-playbook', '-i', maininventory, '--vault-password-file', args.vault_password_file, p])
        if ret == 0:
            logger.info ("ansible-playbook return code: %s", ret)
        else:
            logger.error ("ansible-playbook return code: %s", ret)
            break

def singleplaybook():
    logger.debug ("playbook: %s" % args.playbook)
    # single inventory
    if args.inventory is not None:
        logger.debug ("inventory: %s" % args.inventory)
        checklist = checkplaybooks(args.playbook,args.inventory)
        if not checklist:
            runplaybooks(args.playbook,args.inventory)
    # multi inventory single playbook
    if args.inventories is not None:
        logger.debug ("inventories: %s" % args.inventories)
        checklist = checkplaybooks(args.playbook,args.inventories)
        if not checklist:
            logger.debug ("inventory: %s" % args.inventories[0])
            # run with single playbook, first inventory
            runplaybooks(args.playbook,args.inventories[0])

def multiplaybook():
    logger.debug ("playbooks: %s" % args.playbooks)
    # single inventory
    if args.inventory is not None:
        logger.debug ("inventory: %s" % args.inventory)
        checklist = checkplaybooks(args.playbooks,args.inventory)
        if not checklist:
            runplaybooks(args.playbooks,args.inventory)
    # multi inventory multi playbook
    if args.inventories is not None:
        logger.debug ("inventories: %s" % args.inventories)
        checklist = checkplaybooks(args.playbooks,args.inventories)
        if not checklist:
            logger.debug ("inventory: %s" % args.inventories[0])
            # run with multi playbook, first inventory
            runplaybooks(args.playbooks,args.inventories[0])

# class to watch args.logdir for changes
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
            # actions when a file is first created.
            logger.info ("Received created event - %s." % event.src_path)

        elif event.event_type == 'modified':
            # actions when a file is modified.
            logger.info ("Received modified event - %s." % event.src_path)
            logger.debug ("ssh id: %s" % args.ssh_id)
            logger.debug ("logdir: %s" % args.logdir)
            logger.debug ("interval: %s"  %  str(args.interval))
            logger.debug ("maininventory: $s" % maininventory)
            logger.debug ("workinginventorylist: %s" % workinginventorylist)

            # Additional syntax check of everything if requested
            if args.syntax_check_dir is not None:
                problemlistoutput = checkeverything()
                logger.info ("Playbooks that failed syntax check: " + " ".join(problemlistoutput))
            else:
                problemlistoutput = []

            # single playbook
            if args.playbook is not None and problemlistoutput is None:
                singleplaybook()

            # multiple playbooks
            if args.playbooks is not None and problemlistoutput is None:
                multiplaybook()


if __name__ == '__main__':
    w = Watcher()
    w.run()
