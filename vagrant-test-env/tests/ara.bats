#!/usr/bin/env bats
#
@test "ara homepage responds" {
    run curl http://ansible-master-vagrant/
    [[ "$status" -eq 0 ]]
}

@test "ara has reports" {
    run curl http://ansible-master-vagrant/ | grep "Begin playbook entry in the list"
    [[ "$status" -eq 0 ]]
}
