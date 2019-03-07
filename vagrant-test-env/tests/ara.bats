#!/usr/bin/env bats
#

@test "ara homepage responds" {
    curl -k https://ansible-master-ara:8443/about/ | grep 'ARA Records Ansible'
}

@test "ara has reports" {
    curl -k https://ansible-master-ara:8443/reports/ | grep 'deploy.yaml'
}
