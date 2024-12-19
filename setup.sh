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
