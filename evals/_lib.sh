# shared fixture helpers
gi() { git -c user.email=fixture@skillkeel.com -c user.name=fixture "$@"; }
newrepo() { if [ -n "${1:-}" ]; then rm -rf "$1"; mkdir -p "$1"; cd "$1"; fi; git init -q -b main; }
