#!/usr/bin/env bats
#

@test "ara homepage responds" {
    curl -k -u admin:password https://ansible-master-ara:8443/about/ | grep 'ARA Records Ansible'
}

@test "ara has reports" {
    curl -k -u admin:password https://ansible-master-ara:8443/reports/ | grep 'deploy.yaml'
}

@test "ara page requires a password" {
    run curl -k https://ansible-master-ara:8443/
    [[ "$output" = *"401 Unauthorized"* ]]
}
