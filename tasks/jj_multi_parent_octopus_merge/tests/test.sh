#!/bin/bash

# Use this file to run the tests.
# It will be copied to /tests/test.sh and run from the working directory.

if python3 -m pytest -q /tests/test_final_state.py; then
  echo 1.0 > /logs/verifier/reward.txt
else
  echo 0.0 > /logs/verifier/reward.txt
fi
