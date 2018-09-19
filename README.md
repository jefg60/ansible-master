Role Name
=========

Sets up an ansible master server (should be the only server in a group called ansible-master), creates a git repo for your code on it. Adds git post-update hooks so that this repo is checked out in a "run directory" for running ansible playbooks from.

In my workflow I use one of these per environment (dev/prod/staging etc) with a separate inventory for each. I then push the staging branch of my config management repo to the staging server, and the prod branch to the prod server, etc.

The end result should be that when you push changes to a branch of your configmanagement git repo, they are synced to the run directory on this master ready to be deployed by whatever means you deem appropriate.

If desired, a push to the repo can also trigger a playbook run, which is useful in test environments, for example. To do this, edit templates/post-update.j2 to make the git hook do whatever you like after it has caused changes to propagate to the run dir.

This enables all ansible playbooks to be run from a centrally controlled server whenever changes are pushed to the relevant branch.

This prevents any issues with people running ansible from different hosts, or using different ansible vesions. It also creates a possibility to cron ansible playbook runs.

TODO: make rundeck to create a simplified user interface for deployment.
TODO: make some kind of testing framework on the ansible-master.

Requirements
------------

Ubuntu server 18.04 (LTS) running on the master node.
Of course, you need a working ansible control machine (eg your own) and required ssh keys on the master server so that you can do the initial setup.

Role Variables
--------------

You must set your github username, for fetching your ssh public key. The variable is called github_username.

git_repo_target is the directory where the git repo will be automatically checked out to for ansible to run from

defaults:

github_username: null
git_username: git
git_homedir: /srv/git
git_repo_name: configmanagement
git_repo_target: "/srv/{{ git_repo_name }}"

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
