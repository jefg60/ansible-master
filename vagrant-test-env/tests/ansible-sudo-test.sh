export DISPLAY=:0
export SSH_ASKPASS=/usr/bin/ssh-askpass
ssh-add
ssh ansible@vagrant0 "sudo -n echo"
