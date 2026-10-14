# Work with args in list
args=("$@")

# Handle a-b cases update args and go
for key in "${keys[@]}"; do
  case "$key" in
    a) args+=(--alpha) ;;
    b) args+=(--beta) ;;
    c) args+=(--charlie) ;;
    d) args+=(--delta) ;;
  esac
done

some_command "${args[@]}"

