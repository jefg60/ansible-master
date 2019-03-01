#!/usr/bin/env bats
#

@test "ara homepage responds" {
    curl http://ansible-master-ara/about/ | grep 'ARA Records Ansible'
}

@test "ara has reports" {
    curl http://ansible-master-ara/reports/ | grep 'deploy.yaml'
}
