import requests
import json

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8000/api/v1/recipes/"
TAGS_URL = BASE_URL + "tags/"

TEST_USER = {
    "email": "testuser@example.com",
    "password": "SecurePassword123"
}

# --- Functions ---

def get_auth_token():
    """Logs in and returns the authentication token."""
    login_url = "http://127.0.0.1:8000/api/v1/accounts/login/"
    try:
        response = requests.post(login_url, json=TEST_USER)
        if response.status_code == 200:
            return response.json().get('token')
        else:
            # If login fails, print the failure details
            print(f"Error logging in: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("FATAL ERROR: Server is down. Please start the Django server.")
        return None

def test_authenticated_tags(token):
    """Tests creating and listing Tags."""
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    # 1. Test Creating a Tag
    NEW_TAG = {"name": "Test Tag 1"}
    print("\n--- 1. Testing POST (Create Tag) ---")
    
    try:
        response = requests.post(TAGS_URL, headers=headers, json=NEW_TAG)
        
        if response.status_code == 201: 
            # Success, decode JSON
            print("POST SUCCESS (Tag Created).")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        elif response.status_code == 400:
            # Likely validation error (e.g., tag already exists), decode JSON
            print(f"POST INFO: Status 400 (Validation/Existence Error).")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            # UNEXPECTED ERROR: Print status and raw content for diagnosis
            print(f"POST ERROR: Status {response.status_code}")
            print(f"Raw Response Text (first 200 chars): {response.text[:200]}...")

    except json.JSONDecodeError as e:
        print(f"POST DECODE ERROR: Server returned non-JSON data. Status: {response.status_code}")
        print(f"Raw Response Text (first 200 chars): {response.text[:200]}...")
    except Exception as e:
        print(f"An unexpected Python error occurred during Tag creation: {e}")

    # 2. Test Listing Tags
    print("\n--- 2. Testing GET (List Tags) ---")
    try:
        response = requests.get(TAGS_URL, headers=headers)
        
        if response.status_code == 200:
            # Success, decode JSON
            data = response.json()
            print(f"GET SUCCESS: Retrieved {len(data)} Tags.")
            print("First 3 Tags:")
            print(json.dumps(data[:3], indent=2))
        else:
            # UNEXPECTED ERROR: Print status and raw content for diagnosis
            print(f"GET ERROR: Status {response.status_code}")
            print(f"Raw Response Text (first 200 chars): {response.text[:200]}...")
            
    except json.JSONDecodeError as e:
        print(f"GET DECODE ERROR: Server returned non-JSON data. Status: {response.status_code}")
        print(f"Raw Response Text (first 200 chars): {response.text[:200]}...")
    except Exception as e:
        print(f"An unexpected Python error occurred during Tag listing: {e}")


# --- Main Execution ---
if __name__ == "__main__":
    auth_token = get_auth_token()
    
    if auth_token:
        print("Authentication successful.")
        test_authenticated_tags(auth_token)
    else:
        print("Test failed: Could not retrieve authentication token.")
