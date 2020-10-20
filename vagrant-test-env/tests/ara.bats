#!/usr/bin/env bats
#

@test "ara homepage responds" {
    curl -k -u admin:password https://ansible-master-anmad:8443/ara/about/ | grep 'ARA Records Ansible'
}

@test "ara has reports" {
    curl -k -u admin:password https://ansible-master-anmad:8443/ara/reports/ | grep 'deploy.yaml'
}

@test "ara page requires a password" {
    run curl -kv https://ansible-master-anmad:8443/ara/
    [[ "$output" = *"401 Unauthorized"* ]]
}
