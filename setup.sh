#!/bin/bash

# Function to check if git is installed
check_git_installed() {
  if ! command -v git &> /dev/null; then
    echo ""
    echo "==============================="
    echo "Git is not installed. Please install Git and try again."
    echo "==============================="
    echo ""
    exit 1  # Exit the script if git is not installed
  fi
}

# Function to check if there are uncommitted changes
check_git_status() {
  local status
  status=$(git status --porcelain)  # Get the git status in a clean format
  if [ -n "$status" ]; then
    echo ""
    echo "==============================="
    echo "You have uncommitted changes. Please commit or stash them before pulling."
    echo "==============================="
    echo ""
    exit 1  # Exit the script if there are uncommitted changes
  fi
}

# Function to perform git pull and handle errors
git_pull() {
  echo ""
  echo "==============================="
  echo "Getting the latest version of MentorMatrix's code from GitHub..."
  echo "==============================="
  echo ""

  check_git_status  # Ensure there are no uncommitted changes

  git pull origin main  # Pull from the 'main' branch (or specify the relevant branch)

  if [ $? -ne 0 ]; then
    echo ""
    echo "==============================="
    echo "Git pull failed. Please check for errors."
    echo "==============================="
    echo ""
    exit 1  # Exit if the git pull fails
  fi
}

# Function to check and create .env file if it doesn't exist
create_env_file() {
  if [ ! -f .env ]; then
    echo ""
    echo "==============================="
    echo "Creating .env file..."
    echo "==============================="
    echo ""

    # Prompt the user for the sensitive information
    read -p "Enter your SECRET_KEY (this will be used for Flask sessions and cookies): " SECRET_KEY
    read -p "Enter the path for your UPLOAD_FOLDER (default is 'uploads'): " UPLOAD_FOLDER
    read -p "Enter your DATABASE_URI (default is sqlite:///prod.db): " DATABASE_URI
    read -p "Enter your DEV_DATABASE_URI (default is sqlite:///dev.db): " DEV_DATABASE_URI
    read -p "Enter your TEST_DATABASE_URI (default is sqlite:///test.db): " TEST_DATABASE_URI

    # Force user to provide a valid OpenAI API key
    while [ -z "$OPENAI_API_KEY" ]; do
      read -p "Enter your OPENAI_API_KEY (cannot be empty): " OPENAI_API_KEY
    done

    # Default values if the user doesn't provide any
    SECRET_KEY=${SECRET_KEY:-"your_secret_key_here"}
    UPLOAD_FOLDER=${UPLOAD_FOLDER:-"uploads"}
    DATABASE_URI=${DATABASE_URI:-"sqlite:///prod.db"}
    DEV_DATABASE_URI=${DEV_DATABASE_URI:-"sqlite:///dev.db"}
    TEST_DATABASE_URI=${TEST_DATABASE_URI:-"sqlite:///test.db"}

    # Write the values to .env file
    echo ""
    echo "Writing values to .env file..."
    echo "SECRET_KEY=$SECRET_KEY" > .env
    echo "UPLOAD_FOLDER=$UPLOAD_FOLDER" >> .env
    echo "DATABASE_URI=$DATABASE_URI" >> .env
    echo "DEV_DATABASE_URI=$DEV_DATABASE_URI" >> .env
    echo "TEST_DATABASE_URI=$TEST_DATABASE_URI" >> .env
    echo "OPENAI_API_KEY=$OPENAI_API_KEY" >> .env

    echo ""
    echo "==============================="
    echo ".env file created successfully!"
    echo "==============================="
    echo ""
  else
    echo ""
    echo "==============================="
    echo ".env file already exists. Please ensure it contains the correct values."
    echo "==============================="
    echo ""
  fi
}

# Check if git is installed
check_git_installed

# Execute git pull with error handling
git_pull

# Install Python dependencies
echo ""
echo "==============================="
echo "Installing Python dependencies..."
echo "==============================="
echo ""
pip install -r requirements.txt

# Install JavaScript dependencies
echo ""
echo "==============================="
echo "Installing JS dependencies from package.json..."
echo "==============================="
echo ""
npm install
npm audit fix

# Create .env file if it doesn't exist
create_env_file

# Start the Flask development server
echo ""
echo "==============================="
echo "Starting the development server..."
echo "==============================="
echo ""
flask run
