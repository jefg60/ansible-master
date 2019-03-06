#!/usr/bin/env bats
#

@test "ara homepage responds" {
    curl -k https://ansible-master-ara/about/ | grep 'ARA Records Ansible'
}

@test "ara has reports" {
    curl -k https://ansible-master-ara/reports/ | grep 'deploy.yaml'
}
