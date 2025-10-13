#!/usr/bin/env python3
"""
Deployment script for FJJK Django application.
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def main():
    """Main deployment function."""
    print("🚀 Starting FJJK Django App Deployment")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Please run this script from the backend directory.")
        sys.exit(1)
    
    # Install dependencies
    run_command("pip install -r requirements.txt", "Installing dependencies")
    
    # Run migrations
    run_command("python manage.py migrate", "Running database migrations")
    
    # Collect static files
    run_command("python manage.py collectstatic --noinput", "Collecting static files")
    
    # Check if superuser exists
    print("🔍 Checking for superuser...")
    result = run_command("python manage.py shell -c \"from django.contrib.auth.models import User; print('Superuser exists' if User.objects.filter(is_superuser=True).exists() else 'No superuser found')\"", "Checking superuser")
    
    if result and "No superuser found" in result:
        print("⚠️  No superuser found. You'll need to create one manually:")
        print("   python manage.py createsuperuser")
    
    print("\n✅ Deployment preparation completed!")
    print("\nNext steps:")
    print("1. Choose a deployment platform (Railway, Heroku, or DigitalOcean)")
    print("2. Follow the instructions in DEPLOYMENT.md")
    print("3. Set your environment variables")
    print("4. Deploy your code")

if __name__ == "__main__":
    main()
