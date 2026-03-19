#!/bin/bash
cd /home/user/repo
jj new feature-a feature-b
cat > app.py <<'EOF'
def main():
    print("Feature A")
    print("Feature B")
EOF
jj bookmark move feature-a --to @
