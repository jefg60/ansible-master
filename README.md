Ansible Master
=========

Sets up an ansible master server (should be the only server in a group called ansible-master), creates a git repo for your code on it. Adds git post-update hooks so that this repo is checked out in a "run directory" for running ansible playbooks from. Also provides a browser interface with buttons to run your playbooks from the server, if desired / enabled.

In my workflow I use one of these per environment (dev/prod/staging etc) with a separate inventory for each. I then push the staging branch of my config management repo to the staging server, and the prod branch to the prod server, etc.

The end result should be that when you push changes to a branch of your configmanagement git repo, they are synced to the run directory on this master and can be deployed automatically each time the repo is pushed. Alternatively buttons on the browser interface can be created to run all conifgured playbooks, or individually run one at a time.

A daemon is included that can poll the git log directory for any changes. When the git repo is updated, a line will be added to the log, and the anmad.py daemon will detect this and trigger an ansible run, for the playbooks and secrets etc it is configured to use. See https://github.com/jefg60/anmad for more info.

Example vars for this:

```
start_anmad_daemon: true
anmad_playbooks: "ansible/deploy.yaml ansible/deploy2.yaml"
anmad_prerun: "ansible/ansible-galaxy.yaml ansible/ansible-master.yaml"
```

Using the above configuration, an ansible-galaxy.yaml play is run to fetch roles from ansible-galaxy as defined in a requirements file, then this role is (re)deployed, and if those two both succeed, other playbooks run, potentially in paralell to speed up testing.

The end result is that all ansible playbooks are run from a centrally controlled server whenever changes are pushed to the relevant branch, enabling automated tests of the playbooks when changes are made.

ARA (ARA Records ansible) is a dependency role which will be configured to record all these playbook runs in a database and provide reports in a browser interface.

Requirements
------------

Ubuntu server 18.04 (LTS) running on the master node.
Of course, you need a working ansible control machine (eg your own) and required ssh keys + sudo on the master server so that you can do the initial setup. to add machines to this environment you'll also need someone with ssh and sudo access on them to deploy out ansible-master's ssh keys.

Role Variables
--------------

You must set your github username, for fetching your ssh public key. The variable is called github_username.

git_repo_target is the directory where the git repo will be automatically checked out to for ansible to run from.

defaults:

```yaml
github_username: null
git_username: git
git_homedir: /srv/git
git_repo_name: configmanagement
git_repo_target: "/srv/{{ git_repo_name }}"
git_branch: "master"

anmad_inventory: "{{git_branch}}-inventory"
anmad_vaultpw_file: "~/.vaultpw"
start_anmad_in_screen: false
```

Dependencies
------------
https://github.com/jefg60/ansible-role-ara

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
