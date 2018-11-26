#!/usr/bin/env bats

git_repo_name=configmanagement

@test "The testfile has been pulled to the /srv/configmanagement dir" {
    [ -f /srv/$git_repo_name/testfile ]
}

@test "The testfile contains the success string" {
    grep -qx "git test success" /srv/$git_repo_name/testfile
    [ $? -eq 0 ]
}

