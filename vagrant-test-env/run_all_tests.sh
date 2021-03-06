#!/bin/bash

source /opt/ansible-master/bin/activate

#sleep 120 #ensure time has passed to allow tests to work
bats /vagrant/tests/ | tee /vagrant/tests/results/TAP

#This causes us to exit with the exit code of the bats not the tee
exit ${PIPESTATUS[0]}
