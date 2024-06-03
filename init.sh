shell=$(ps -cp "$$" -o command="")
if [ "$shell" = "zsh" ] || [ "$shell" = "-zsh" ]; then
  SCRIPT_FILE="${(%):-%N}"
  SCRIPT_DIR="${SCRIPT_FILE:a:h}"
elif [ "$shell" = "bash" ] || [ "$shell" = "-bash" ]; then
  SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
else
  echo "git_commands: unsupported shell: $shell" >&2
  return
fi

original_git=$(which git)

# Intercept git commands
function git() {
  result=$("$SCRIPT_DIR/bin/python3" "$SCRIPT_DIR/git_override.py" "$@")
  if [ $? -eq 0 ]; then
    eval "$original_git" $result
  fi
}
