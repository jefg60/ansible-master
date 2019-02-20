#!/usr/bin/env bats

git_repo_name=configmanagement

@test "The testfile has been pulled to the /srv/configmanagement dir" {
    [ -f /srv/$git_repo_name/testfile ]
}

@test "The testfile contains a 1 to 5 digit number" {
    grep -qx "[0-9]\{1,5\}" /srv/$git_repo_name/testfile
    [ $? -eq 0 ]
}

