#!/usr/bin/env bats
#
@test "noninteractive shell message" {
    run sudo su - git
    [[ "$output" = *"provide interactive shell access"* ]]
}

@test "try to run ansible as git and check it fails" {
    run sudo su -c "ansible --version" git
    [[ "$status" -eq 128 ]]
}
