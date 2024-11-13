#!/bin/bash

if [ -z "$1" ]; then
  echo "Please provide a commit message."
  echo "Example format: ./push.sh \"your message\""
  exit 1
fi

commit_message="$1"
echo "Pushing code"
echo "     "
echo "     "

git add .
git commit -m "$commit_message"
git push

echo "     "
echo "     "
echo "     "
echo "Commit message: $commit_message"
echo "Code pushed successfully, happy hunting"

