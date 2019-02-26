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
