#!/usr/bin/env bats
#
@test "vagrant version" {
    run vagrant --version
    [[ "$output" =~ "Vagrant 2.2." ]]
}

