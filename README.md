Ansible Master
=========

Sets up an ansible master server (should be the only server in a group called ansible-master), creates a git repo for your code on it. Adds git post-update hooks so that this repo is checked out in a "run directory" for running ansible playbooks from. Also provides a browser interface with buttons to run your playbooks from the server. See https://github.com/jefg60/anmad for more info on that.

In my workflow I use one of these per environment (dev/prod/staging etc) with a separate inventory for each. I then push the staging branch of my config management repo to the staging server, and the prod branch to the prod server, etc.

The end result should be that when you push changes to a branch of your configmanagement git repo, they are synced to the run directory on this master and can be deployed automatically each time the repo is pushed. Buttons on the browser interface are created to run all configured playbooks, or individually run one at a time.

Example vars:

```
anmad_playbooks:
  - deploy.yaml
  - deploy2.yaml
anmad_prerun:
  - ansible-galaxy.yaml
  - ansible-master.yaml
```

Using the above configuration, an ansible-galaxy.yaml play is run to fetch roles from ansible-galaxy as defined in a requirements file, then this role is (re)deployed, and if those two both succeed, other playbooks run, potentially in paralell to speed up testing (default concurrency is number of cpus reported by the OS).

The end result is that all ansible playbooks are run from a centrally controlled server whenever changes are pushed to the relevant branch, enabling automated tests of the playbooks when changes are made.

ARA (ARA Records ansible) is a dependency role which will be configured to record all these playbook runs in a database and provide reports in a browser interface. A button is created on the interface to link to these reports.

Requirements
------------

Ubuntu server 18.04 (LTS) running on the master node.
Of course, you need a working ansible control machine (eg your own) and required ssh keys + sudo on the master server so that you can do the initial setup. To add machines to this environment you'll also need someone with ssh and sudo access on them to deploy out ansible-master's ssh keys.

Role Variables
--------------

You must set your github username, for fetching your ssh public key. The variable is called github_username.

git_repo_target is the directory where the git repo will be automatically checked out to for ansible to run from.

syntax_check_dir: directory to scan for .yml or .yaml files on each run and syntax check all of them against your configured inventories. Leave undefined to disable this behaviour.

master_ansible_user_ssh_phrase: use to set a passphrase on the master ansible user's ssh private key. To ensure that the anmad daemons which run playbooks are able to start, you'll need to ensure that the vault password file is set and that you have included a vault which contains master_ansible_user_ssh_phrase in the anmad config variable master_ansible_user_vaultfile.

Hopefully the role defaults file will explain the default vars. Of note is ara_override which is used to configure the ARA role. To override of these, you'll need to populate all of ara_override in your own vars files.

Dependencies
------------
https://github.com/jefg60/ansible-role-ara
https://github.com/jefg60/ansible-orchestration-linux
https://github.com/jefg60/anmad

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: ansible-master
      roles:
         - { role: jefg60.ansible-master, github_username: jefg60 }

License
-------

GPLv3

Author Information
------------------

Jeff Hibberd
