#!/usr/bin/env bats
#
@test "logpoll version 0.7" {
    run ansible-logpoll.py --version
    [[ "$output" = "0.7" ]]
}

