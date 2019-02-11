#!/usr/bin/env bats
#
@test "logpoll version 0.5" {
    run ansible-logpoll.py --version
    [[ "$output" = "0.5" ]]
}

