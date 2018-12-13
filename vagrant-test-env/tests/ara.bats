#!/usr/bin/env bats
#

# first reload ara service to pick up changes to the db in the web app
sudo service ara restart
sleep 2

@test "ara homepage responds" {
    curl http://127.0.0.1:9191/about/ | grep 'ARA Records Ansible'
}

@test "ara has reports" {
    curl http://127.0.0.1:9191/reports/ | grep 'deploy.yaml'
}
