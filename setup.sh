#!/bin/bash

# Function to check if git is installed
check_git_installed() {
  if ! command -v git &>/dev/null; then
    echo ""
    echo "==============================="
    echo "Git is not installed. Please install Git and try again."
    echo "==============================="
    echo ""
    exit 1 # Exit the script if git is not installed
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

    # Prompt the user for Google OAuth credentials
    while [ -z "$GOOGLE_CLIENT_ID" ]; do
      read -p "Enter your GOOGLE_CLIENT_ID (cannot be empty): " GOOGLE_CLIENT_ID
    done

    while [ -z "$GOOGLE_CLIENT_SECRET" ]; do
      read -p "Enter your GOOGLE_CLIENT_SECRET (cannot be empty): " GOOGLE_CLIENT_SECRET
    done

    while [ -z "$GOOGLE_DISCOVERY_URL" ]; do
      read -p "Enter your GOOGLE_DISCOVERY_URL (cannot be empty): " GOOGLE_DISCOVERY_URL
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
    echo "SECRET_KEY=$SECRET_KEY" >.env
    echo "UPLOAD_FOLDER=$UPLOAD_FOLDER" >>.env
    echo "DATABASE_URI=$DATABASE_URI" >>.env
    echo "DEV_DATABASE_URI=$DEV_DATABASE_URI" >>.env
    echo "TEST_DATABASE_URI=$TEST_DATABASE_URI" >>.env
    echo "OPENAI_API_KEY=$OPENAI_API_KEY" >>.env
    echo "GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID" >>.env
    echo "GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET" >>.env
    echo "GOOGLE_DISCOVERY_URL=$GOOGLE_DISCOVERY_URL" >>.env

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

# Fixing errors
echo ""
echo "==============================="
echo "Fixing potential errors..."
echo "==============================="
echo ""
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
