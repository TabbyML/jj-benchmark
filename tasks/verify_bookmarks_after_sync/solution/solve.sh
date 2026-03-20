#!/bin/bash
set -euo pipefail

cd /home/user/repo
jj git fetch
jj bookmark move feature-x --to feature-x@origin
