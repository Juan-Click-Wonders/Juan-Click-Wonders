"""
Simple script to test the 404 page.
Run this script with Django's development server running.
"""

import requests

def test_404_page():
    """Test the 404 page by requesting a non-existent URL."""
    url = "http://127.0.0.1:8000/this-page-does-not-exist"
    response = requests.get(url)
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 404:
        print("Successfully received a 404 response!")
        print("Response content preview:")
        print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
    else:
        print(f"Unexpected status code: {response.status_code}")

if __name__ == "__main__":
    test_404_page()
