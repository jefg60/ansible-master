#!/usr/bin/env bats
#
version=0.11.1

@test "anmad_buttons version $version" {
    run /opt/ansible-master/bin/python3 /srv/anmad/anmad_buttons.py --version
    [[ "$output" = "$version" ]]
}

@test "anmad_buttons control page has a deploy2.yaml button" {
    curl -k -u admin:password https://ansible-master-control:8443/ | grep 'deploy2.yaml'
}

@test "anmad_buttons has its own log file" {
    sudo grep INFO /var/log/anmad_buttons
}

@test "anmad buttons control page requires authentication" {
    run curl -k https://ansible-master-control:8443/
    [[ "$output" = *"401 Unauthorized"* ]]
}

@test "anmad_run service is running" {
    sudo service anmad_run status
}
