#!/bin/bash
# Update git repositories in the mount folder.
# As the mount folder is shared, this script can be run on either the host or the container.
# Adapated from https://gist.github.com/douglas/1287372

# store the current dir
CUR_DIR=$(pwd)

echo ">>> Pulling in latest changes for all repositories..."

# Find all git repositories and update the checked out branch to latest revision
for i in $(find ./../../mount/github-repos -name ".git" | cut -c 3-); do
    echo "";
    echo ">>> "+$i;

    # We have to go to the .git parent directory to call the pull command
    cd "$i";
    cd ..;

    git pull --rebase;

    # lets get back to the CUR_DIR
    cd $CUR_DIR
done

echo ">>> Complete!"