#!/usr/bin/python3
import argparse
import subprocess
import ssh_agent_setup
import time
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


parser = argparse.ArgumentParser()
parser.add_argument("--inventory", help="ansible inventory to use", required=True)
parser.add_argument("--playbook", help="ansible playbook to run", required=True)
parser.add_argument("--interval", help="interval in seconds at which to check for new code", default=15)
parser.add_argument("--ssh_id", help="ssh id file to use", default=".ssh/id_rsa")
parser.add_argument("--logdir", help="log dir to watch", default="/srv/git/log")
args = parser.parse_args()

print(datetime.datetime.now(), "ansible-runner STARTED")
print ("ssh id: " + args.ssh_id)
print ("logdir: " + args.logdir)
print ("inventory: " + args.inventory)
print ("playbook: " + args.playbook)
print ("interval: "  +  str(args.interval))
#exit()

#add ssh key to agent (passphrase will be prompted for if required)
ssh_agent_setup.setup()
ssh_agent_setup.addKey( args.ssh_id )

# class to watch /srv/git/ for changes and run ansible playbook when changes occur
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
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print(datetime.datetime.now(), "Received created event - %s." % event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print(datetime.datetime.now(), "Received modified event - %s." % event.src_path)
            print ("ssh id: " + args.ssh_id)
            print ("logdir: " + args.logdir)
            print ("inventory: " + args.inventory)
            print ("playbook: " + args.playbook)
            print ("interval: "  +  str(args.interval))
            print ("Attempting to run ansible-playbook -i ", args.inventory, args.playbook)
            ret = subprocess.call(['ansible-playbook', '-i', args.inventory, args.playbook])
            print (datetime.datetime.now(), "ansible-playbook return code:", ret)


if __name__ == '__main__':
    w = Watcher()
    w.run()
