# shared fixture helpers
gi() { git -c user.email=fixture@skillkeel.com -c user.name=fixture "$@"; }
newrepo() { rm -rf "$1"; mkdir -p "$1"; cd "$1"; git init -q -b main; }
