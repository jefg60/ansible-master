Ansible Master
=========

Sets up an ansible master server (should be the only server in a group called ansible-master), creates a git repo for your code on it. Adds git post-update hooks so that this repo is checked out in a "run directory" for running ansible playbooks from.

In my workflow I use one of these per environment (dev/prod/staging etc) with a separate inventory for each. I then push the staging branch of my config management repo to the staging server, and the prod branch to the prod server, etc.

The end result should be that when you push changes to a branch of your configmanagement git repo, they are synced to the run directory on this master ready to be deployed by whatever means you deem appropriate.

A python daemon is included that runs in a screen session polling the git log directory for any changes. When the git repo is updated, a line will be added to the log, and the ansible-logpoll.py daemon will detect this and trigger an ansible run. Screen is used because ansible-logpoll.py will prompt for a passphrase if you've set one on the ssh key, so screen is the current workaround to enable you to attach and type this. Note that if a screen called ansible-logpoll already exists, no new screen sessions are started. This is to prevent ansible killing itself. This screen daemon situation and the self updating aspect are still a work in progress, obviously!

The daemon accepts a list of playbooks to run in order and will stop processing if one fails.

Example vars for this:

```
start_ansible_logpoll_in_screen: true
ansible_logpoll_playbooks: "ansible/ansible-galaxy.yaml ansible/ansible-master.yaml ansible/deploy.yaml"
```

Using the above configuration, an ansible-galaxy.yaml play is run to fetch roles from ansible-galaxy as defined in a requirements file, then this role is (re)deployed, and if those two both succeed, a playbook called deploy.yaml runs (in my case, deploy.yaml is a list of import_playbook statements that deploys my entire environment).

The end result is that all ansible playbooks are run from a centrally controlled server whenever changes are pushed to the relevant branch.

This prevents any issues with people running ansible from different hosts, or using different ansible vesions. It also creates a possibility to cron ansible playbook runs. If you make it run all of your playbooks with each push, then it also prevents configuration drift. I recommend including a playbook that runs tests against your environment, if you do this.

Requirements
------------

Ubuntu server 18.04 (LTS) running on the master node.
Of course, you need a working ansible control machine (eg your own) and required ssh keys + sudo on the master server so that you can do the initial setup.

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

ansible_logpoll_inventory: "{{git_branch}}-inventory"
ansible_logpoll_vaultpw_file: "~/.vaultpw"
start_ansible_logpoll_in_screen: false
```

Dependencies
------------


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
