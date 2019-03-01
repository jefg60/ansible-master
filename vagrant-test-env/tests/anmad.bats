#!/usr/bin/env bats
#
version=0.10.1

@test "anmad_dirpoll version $version" {
    run /opt/ansible-master/bin/python3 /srv/anmad/anmad_dirpoll.py --version
    [[ "$output" = "$version" ]]
}

@test "anmad_dirpoll has its own log file" {
    sudo grep INFO /var/log/anmad_dirpoll
}

@test "anmad_buttons version $version" {
    run /opt/ansible-master/bin/python3 /srv/anmad/anmad_buttons.py --version
    [[ "$output" = "$version" ]]
}

@test "anmad_buttons has its own log file" {
    sudo grep INFO /var/log/anmad_buttons
}

@test "anmad_buttons control page has a deploy2.yaml button" {
    curl -k -u admin:password https://ansible-master-control/ | grep 'deploy2.yaml'
}

@test "anmad_dirpoll service is running" {
    sudo service anmad_dirpoll status
}

@test "anmad_run service is running" {
    sudo service anmad_run status
}
