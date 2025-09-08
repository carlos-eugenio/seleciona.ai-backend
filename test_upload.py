#!/usr/bin/env python3
"""
Test script for file upload functionality
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
TEST_FILE = "test_emails.txt"

def test_file_upload():
    """Test the file upload endpoint"""
    
    # First, you would need to login to get a token
    # This is just a demonstration of how to use the upload endpoint
    
    print("File Upload Test Script")
    print("=" * 50)
    
    # Example of how to use the upload endpoint
    print("1. Upload single file:")
    print(f"   curl -X POST '{BASE_URL}/api/upload/emails' \\")
    print("     -H 'Authorization: Bearer YOUR_TOKEN' \\")
    print(f"     -F 'file=@{TEST_FILE}'")
    print()
    
    print("2. Upload multiple files:")
    print(f"   curl -X POST '{BASE_URL}/api/upload/emails/multiple' \\")
    print("     -H 'Authorization: Bearer YOUR_TOKEN' \\")
    print(f"     -F 'files=@{TEST_FILE}' \\")
    print("     -F 'files=@another_file.txt'")
    print()
    
    print("3. File format should be:")
    print("   email@example.com|Subject|Message content")
    print("   another@example.com|Another Subject|Another message")
    print()
    
    print("4. Supported file types: .txt, .pdf")
    print()
    
    print("5. Example response:")
    example_response = {
        "success": True,
        "message": "Successfully processed 2 emails",
        "processed_count": 2,
        "file_name": "test_emails.txt"
    }
    print(json.dumps(example_response, indent=2))

if __name__ == "__main__":
    test_file_upload() 