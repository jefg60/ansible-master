#!/usr/bin/env bats
#
@test "ara homepage responds" {
    curl http://127.0.0.1:9191/about/ | grep 'ARA Records Ansible'
}

@test "ara has reports" {
    curl http://127.0.0.1:9191/reports/ | grep 'deploy.yaml'
}
