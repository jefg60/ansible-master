#!/usr/bin/env bats
#
version=0.9.4

@test "logpoll version $version" {
    run ansible-logpoll.py --version
    [[ "$output" = "$version" ]]
}

@test "logpoll screen can start up" {
    ansible-logpoll-screen.sh
    run screen -ls ansible-logpoll
    [ "$status" -eq 0 ]
}

@test "logpoll has its own log file" {
    sudo grep INFO /var/log/ansible-logpoll
}
