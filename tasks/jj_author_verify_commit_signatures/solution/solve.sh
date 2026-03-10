#!/bin/bash

# Configure globally
jj config set --user signing.backend "gpg"
jj config set --user signing.key "signing@example.com"
jj config set --user signing.behavior "own"
jj config set --user ui.show-cryptographic-signatures true

cd /home/user/repo
jj new
echo "signed content" > signature_test.txt
jj describe -m "Add signature test file"
jj log -r @ -T 'commit_id.short() ++ " " ++ if(signature, signature.status(), "no sig") ++ "\n"' > /home/user/signature_verification.log
