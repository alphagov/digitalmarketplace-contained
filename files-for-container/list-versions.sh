#!/bin/bash
# List languages and backend services versions

python3 --version
pip --version
echo Node "$(node --version)"
nginx -v
psql --version
redis-cli --version
