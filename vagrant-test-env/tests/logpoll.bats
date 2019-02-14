#!/usr/bin/env bats
#
@test "logpoll version 0.8" {
    run ansible-logpoll.py --version
    [[ "$output" = "0.8" ]]
}

@test "logpoll screen can start up" {
    ansible-logpoll-screen.sh
    run screen -ls ansible-logpoll
    [ "$status" -eq 0 ]
}
