#!/usr/bin/env bats
#
#This is obviously just a quick control test - if this fails the tests are not reliable!

@test "Check that 1 equals 1" {
    one=1
    [ $one -eq 1 ]
}

