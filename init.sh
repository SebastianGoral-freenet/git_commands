#!/usr/bin/env bash

original_git=$(which git)
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Intercept git commands
function git() {
  result=$(python3 "$SCRIPT_DIR/git_override.py" "$@")
  if [ $? == 0 ]; then
    eval "$original_git" $result
  fi
}