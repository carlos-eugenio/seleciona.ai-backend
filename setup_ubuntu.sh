#!/bin/bash

# Seleciona AI Backend - Ubuntu/Debian Setup Script
# This script automates the installation process

set -e  # Exit on any error

echo "🚀 Seleciona AI Backend - Ubuntu/Debian Setup"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root for security reasons"
   exit 1
fi

# Update system
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
print_status "Installing Python and system dependencies..."
sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential libssl-dev libffi-dev pkg-config git

# Install MySQL
print_status "Installing MySQL..."
sudo apt install -y mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql

# Install MySQL client libraries
print_status "Installing MySQL client libraries..."
sudo apt install -y libmysqlclient-dev || sudo apt install -y libmariadb-dev-compat libmariadb-dev

# Create virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
python -m pip install --upgrade pip

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file
print_status "Creating environment configuration..."
if [ ! -f .env ]; then
    cp env.example .env
    print_warning "Created .env file from template. Please edit it with your database credentials."
else
    print_status ".env file already exists."
fi

# Create uploads directory
print_status "Creating uploads directory..."
mkdir -p uploads/avatars

# Database setup
echo ""
print_status "Database setup required:"
echo "Run the following command to create the database and user:"
echo ""
echo "sudo mysql -e \"CREATE DATABASE seleciona_ai_db; CREATE USER 'seleciona_user'@'localhost' IDENTIFIED BY 'seleciona_password'; GRANT ALL PRIVILEGES ON seleciona_ai_db.* TO 'seleciona_user'@'localhost'; FLUSH PRIVILEGES;\""
echo ""

# Generate JWT secret key
print_status "Generating JWT secret key..."
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
print_status "Generated SECRET_KEY: $SECRET_KEY"
print_warning "Please update your .env file with this secret key"

# Make setup script executable
chmod +x setup_ubuntu.sh

print_status "Setup completed successfully! 🎉"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Create database (see command above)"
echo "3. Update .env file with your SECRET_KEY: $SECRET_KEY"
echo "4. Run migrations: alembic upgrade head"
echo "5. Start application: python main.py"
echo ""
echo "For detailed instructions, see INSTALLATION_UBUNTU.md"
