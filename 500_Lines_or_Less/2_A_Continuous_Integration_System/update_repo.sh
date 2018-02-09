#!/bin/bash

# After running this bash script
#   - if there is a new commit, the script create a .commit_id file
#   - otherwise, the .commit_id file does not exist

# This is like "import", include run or fail helper method.
# This method is used to run the given command, or fail with the given error message.
source run_or_fail.sh


# .commit_id is the file containing the newest commit_id. It only been created when a new commit appears.
bash rm -f .commit_id

# verify the repo we are observing exists
# and reset it to the newest commit
run_or_fail "Repository folder not found!" pushed $1 1> /dev/null
run_or_fail "Could not reset git" git reset --hard HEAD

# Get the newest commit id
COMMIT=$(run_or_fail "Could not call 'git log' on repository" git log -n1)
if [ $? != 0 ]; then
    echo "Could not call 'git log' on repository"
    exit 1
fi
COMMIT_ID=`echo $COMMIT | awk '{ print $2 }'`

# Pulls the repository and gets the most recent commit id
run_or_fail "Could not pull from repository" git pull
COMMIT=$(run_or_fail "Could not call 'git log' on repository" git log -n1)
if [ $? != 0 ]; then
  echo "Could not call 'git log' on repository"
  exit 1
fi
NEW_COMMIT_ID=`echo $COMMIT | awk '{ print $2 }'`

# If the commit id does not match the previous ID, write to .commit_id file
if [ $NEW_COMMIT_ID != $COMMIT_ID ]; then
  popd 1> /dev/null
  echo $NEW_COMMIT_ID > .commit_id
fi
