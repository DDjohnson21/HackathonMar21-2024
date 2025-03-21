#!/bin/bash

# Script to synchronize changes in a shared Codespace

# Function to print messages
print_message() {
  echo -e "\n========================================"
  echo "$1"
  echo "========================================\n"
}

# Step 1: Pull latest updates from the remote repository
print_message "Pulling updates from the remote repository..."
git pull origin main

# Step 2: Check for merge conflicts
if [ $? -ne 0 ]; then
  print_message "Merge conflicts detected! Please resolve them manually and rerun the script."
  exit 1
fi

# Step 3: Add all local changes
print_message "Staging all local changes..."
git add .

# Step 4: Commit local changes
print_message "Committing local changes..."
read -p "Enter commit message: " commit_message
git commit -m "$commit_message"

# Step 5: Push changes to the remote repository
print_message "Pushing changes to the remote repository..."
git push origin main

# Final message
if [ $? -eq 0 ]; then
  print_message "Synchronization complete! Changes have been pushed to the main branch."
else
  print_message "Error occurred during the push. Please check your connection and repository access."
fi