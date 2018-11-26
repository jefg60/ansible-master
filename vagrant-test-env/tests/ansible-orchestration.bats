#!/usr/bin/env bats
#
@test "ansible ping" {
    run sudo su -c /vagrant/ansible-ping.sh ansible
    [[ "$status" -eq 0 ]]
}

@test "Test that we CANNOT ssh as ansible without the key" {
    run ssh ansible@vagrant0 exit
    [[ "$status" -eq 255 ]]
}

@test "Ansible user can sudo with no password on master" {
    run sudo -u ansible sudo -n echo
    [[ "$status" -eq 0 ]]
}

@test "Ansible user can sudo with no password on clients" {
    run sudo su -c /vagrant/ansible-sudo-test.sh ansible
    [[ "$status" -eq 0 ]]
}

@test "a logfile is created in /srv/git/log/ when a push happens" {
    [[ -e /srv/git/log/configmanagement.log ]]
}

@test "first ansible-playbook runs when git repo is pushed" {
    [[ -s /srv/success.txt ]]
}

@test "second ansible-playbook runs when git repo is pushed" {
    [[ -s /srv/success2.txt ]]
}

@test "deploy.yaml gets pushed correctly to /srv/configmanagement" {
    run diff /home/vagrant/testdata/ansible/deploy.yaml /srv/configmanagement/ansible/deploy.yaml
    [[ "$status" -eq 0 ]]
}

@test "ansible user is running a screen" {
    run sudo su -c "screen -ls" ansible
    [[ "$status" -eq 0 ]]
}

