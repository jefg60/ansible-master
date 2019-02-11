#!/usr/bin/env bats
#
@test "vagrant version 2.2" {
    run vagrant --version
    [[ "$output" =~ "Vagrant 2.2." ]]
}

