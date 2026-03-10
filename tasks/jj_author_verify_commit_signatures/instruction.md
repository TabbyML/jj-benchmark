You are an OS engineer comparing how `jj` (Jujutsu) handles commit signatures compared to Git. You have a repository located at `/home/user/repo` which is already initialized with `jj`.

Your task is to:
1. Configure `jj` globally to sign commits authored by you using GPG. The GPG key has already been created and is associated with the email address `signing@example.com`.
2. Enable the display of cryptographic signatures in `jj` UI globally.
3. Create a new commit with the description "Add signature test file" that adds a file named `signature_test.txt` containing the text `signed content`.
4. Verify the signature of the commit you just created and save the output of the `jj log` command showing the signature status into a file named `/home/user/signature_verification.log`. 
   Use the following command to format the log output specifically for verification:
   `jj log -r @ -T 'commit_id.short() ++ " " ++ if(signature, signature.status(), "no sig") ++ "\n"' > /home/user/signature_verification.log`

Note: You do not need to install GPG or `jj`, they are already installed. You just need to configure `jj` and perform the operations.
