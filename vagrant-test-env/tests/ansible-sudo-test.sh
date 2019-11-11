export DISPLAY=:0
export SSH_ASKPASS=/usr/bin/ssh-askpass
ssh-add
ssh ansible@ansible-master-vagrant-client "sudo -n echo"
