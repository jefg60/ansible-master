#!/bin/bash
export SSH_ASKPASS=/usr/bin/ssh-askpass
export DISPLAY=:0
eval $(ssh-agent -s)
nohup ssh-add
/opt/ansible-master/bin/ansible all -i /vagrant/inventory-internal -m ping
