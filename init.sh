#!/usr/bin/env bash

original_git=$(which git)

# Intercept git commands
function git() {
  result=$(/Users/sebastiangoral/workspace/git_commands/venv/bin/python /Users/sebastiangoral/workspace/git_commands/git_override.py "$@")
  if [ $? == 0 ]; then
    eval "$original_git" $result
  fi
}