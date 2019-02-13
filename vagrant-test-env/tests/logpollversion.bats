#!/usr/bin/env bats
#
@test "logpoll version 0.6" {
    run ansible-logpoll.py --version
    [[ "$output" = "0.6" ]]
}

