#!/bin/bash
# $1 will be the network range passed by vagrant

# if we have already done this, exit
grep -q $1 /etc/hosts && exit 0

# build the hosts file
echo "$1"12 vagrant0 >>/etc/hosts 
echo "$1"13 ansible-master-vagrant >>/etc/hosts

grep $1 /etc/hosts && exit 0
