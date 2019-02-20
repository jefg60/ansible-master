#!/usr/bin/env bats
#
version=0.9.4

@test "logpoll version $version" {
    run /opt/ansible-master/bin/python3 /srv/ansible-logpoll/ansible_logpoll.py --version
    [[ "$output" = "$version" ]]
}

@test "logpoll has its own log file" {
    sudo grep INFO /var/log/ansible-logpoll
}
