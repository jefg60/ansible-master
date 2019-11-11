#!/bin/bash
# $1 will be the network range passed by vagrant

# if we have already done this, exit
grep -q $1 /etc/hosts && exit 0

# build the hosts file
echo "$1"12 ansible-master-vagrant-client >>/etc/hosts
echo "$1"13 ansible-master-vagrant-server >>/etc/hosts
echo "$1"13 ansible-master-ara >>/etc/hosts
echo "$1"13 ansible-master-control >>/etc/hosts

grep $1 /etc/hosts && exit 0
