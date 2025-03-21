#!/bin/bash

# Script to fetch updates from Git, merge with local changes, and push updates to main

# Function to print messages
print_message() {
  echo -e "\n========================================"
  echo "$1"
  echo "========================================\n"
}

# Step 1: Fetch updates from remote
print_message "Fetching updates from remote repository..."
git fetch origin

# Step 2: Merge updates from remote main branch
print_message "Merging updates from 'origin/main' into the current branch..."
git merge origin/main

# Step 3: Check for conflicts
if [ $? -ne 0 ]; then
  print_message "Merge conflicts detected! Please resolve them and rerun the script."
  exit 1
fi

# Step 4: Add all local changes
print_message "Adding all local changes..."
git add .

# Step 5: Commit local changes
print_message "Committing local changes..."
read -p "Enter commit message: " commit_message
git commit -m "$commit_message"

# Step 6: Push changes to main
print_message "Pushing changes to the 'main' branch..."
git push origin main

# Final message
if [ $? -eq 0 ]; then
  print_message "Updates successfully pushed to 'main'."
else
  print_message "Error occurred while pushing updates. Please check your setup."
fi

#In each Git repository where you want to use Git LFS, select the file types you'd like Git LFS to manage (or directly edit your .gitattributes). You can configure additional file extensions at anytime.

#git lfs track "*.psd"
#Now make sure .gitattributes is tracked:

#git add .gitattributes
#Note that defining the file types Git LFS should track will not, by itself, convert any pre-existing files to Git LFS, such as files on other branches or in your prior commit history. To do that, use the git lfs migrate(1) command, which has a range of options designed to suit various potential use cases.

#There is no step three. Just commit and push as you normally would; for instance, if your current branch is named main:

#it add file.psd
#git commit -m "Add design file"
#git push origin main