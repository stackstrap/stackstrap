#!/bin/sh
#
# StackStrap - Loose SSH wrapper
# https://github.com/openops/stackstrap
#
# This script is a wrapper around the ssh binary that turns off strict host
# key checking so that when we're using GIT over ssh we don't get prompted to
# accept host keys.
#

exec ssh -o StrictHostKeyChecking=no $*
