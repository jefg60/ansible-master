#!/usr/bin/env bats
#
version=0.21.0

@test "anmad version $version" {
    run /opt/ansible-master/bin/python3 -m anmad.interface --version
    [[ "$output" = *"$version" ]]
}

@test "anmad interface page has correct version $version" {
    curl -k -u admin:password https://ansible-master-anmad:8443/ | grep $version
}

@test "anmad interface page has a deploy2.yaml button" {
    curl -k -u admin:password https://ansible-master-anmad:8443/ | grep 'deploy2.yaml'
}

@test "anmad interface has its own log file" {
    sudo grep INFO /var/log/anmad/interface.log
}

@test "anmad daemon has its own log file" {
    sudo grep INFO /var/log/anmad/daemon.log
}

@test "anmad interface page requires authentication" {
    run curl -kv https://ansible-master-anmad:8443/
    [[ "$output" = *"401 Unauthorized"* ]]
}

@test "anmad service is running" {
    sudo service anmad status
}

@test "deploy2.yaml.log exists" {
  run compgen -G /var/log/ansible/playbook/deploy2.yaml/*/deploy2.yaml.*.log
  [ "$status" -eq 0 ]
}
