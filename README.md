Role Name
=========

Sets up an ansible master server (should be the only server in a group called ansible-master), creates a git repo for your code on it.

In my workflow I use one of these per environment (dev/prod/staging etc) with a separate inventory for each. I then push the staging branch of my config management repo to the staging server, and the prod branch to the prod server, etc.

TODO: make git hooks to sync the repo with a folder in the ansible user's home dir, for running the orchestration playbooks from this ansible-master host. without this, one must git clone the repo from the git user's filesystem to the ansible user's home dir and git pull from the ansible user, after pushing any changes.

The end result should be that when you push changes to a branch of your configmanagement git repo, they are synced to the ansible user on this master ready to be deployed. If desired, a push to the repo can also trigger a playbook run, which is useful in test environments, for example.

This enables all ansible playbooks to be run from a centrally controlled server, regardless of who runs it, as long as they have a way to become the ansible user after authenticating, or they allow the git hooks to automatically run the playbooks when they are pushed the relevant branch. 

This prevents any issues with people running ansible from different hosts, as different users or using incorrect ansible vesions. Once all this is set up you should be able to remove any access for these users to directly interact with the managed nodes, and thereby force them to use the ansible master to run your playbooks from a controlled environment.

TODO: make rundeck to create a simplified user interface for deployment.
TODO: make some kind of testing framework on the ansible-master.

Requirements
------------

Ubuntu server 18.04 (LTS) running on the master node.
Of course, you need a working ansible control machine (eg your own) and required ssh keys on the master server so that you can do the initial setup.

Role Variables
--------------

You must set your github username, for fetching your ssh public key. The variable is called github_username.

defaults:

github_username: null
git_username: git
git_homedir: /srv/git
git_repo_name: configmanagement

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
