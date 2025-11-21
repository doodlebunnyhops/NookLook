#!/usr/bin/env python3
"""
Full Nookipedia URL synchronization script.
This script fetches URLs from Nookipedia and updates the database in one go.
"""

import sys
import os
from pathlib import Path

# Try to load dotenv, but don't fail if not available
try:
    from dotenv import load_dotenv
    load_dotenv()  # This will automatically look for .env file
except ImportError:
    print("Note: python-dotenv not installed. Install with: pip install python-dotenv")
    print("Falling back to system environment variables only.")

def main():
    """Run the complete Nookipedia URL sync process."""
    
    # Check for API key
    api_key = os.getenv('NOOKIPEDIA_API')
    if not api_key:
        print("Error: NOOKIPEDIA_API environment variable not set")
        print("Please either:")
        print("1. Set it as a system environment variable")
        print("2. Create a .env file in the project root with: NOOKIPEDIA_API=your-key-here")
        return 1
    
    script_dir = Path(__file__).parent
    
    print("Starting Nookipedia URL synchronization...")
    print("=" * 50)
    
    # Step 1: Fetch URLs
    print("Step 1: Fetching URLs from Nookipedia API...")
    fetch_script = script_dir / "fetch_urls.py"
    result = os.system(f"python {fetch_script}")
    
    if result != 0:
        print("URL fetching failed!")
        return 1

    print("\n" + "=" * 50)

    # Step 2: Update database
    print("Step 2: Updating database with fetched URLs...")
    update_script = script_dir / "update_db.py"
    result = os.system(f"python {update_script}")
    
    if result != 0:
        print("Database update failed!")
        return 1

    print("\n" + "=" * 50)
    print("Nookipedia URL synchronization completed successfully!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())