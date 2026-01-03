import requests
import json

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8000/api/v1/accounts/"
REGISTER_URL = BASE_URL + "register/"
LOGIN_URL = BASE_URL + "login/"

# Define the user to register and log in
TEST_USER = {
    "email": "testuser@example.com",
    "name": "Test User",
    "password": "SecurePassword123"
}

# --- Functions ---

def register_user():
    """Attempts to register a new user."""
    print("--- 1. Attempting to Register New User ---")
    try:
        response = requests.post(REGISTER_URL, json=TEST_USER)
        data = response.json()
        
        if response.status_code == 200:
            print(f"SUCCESS: User registered and logged in.")
            print(f"User ID: {data['user']['id']}")
            print(f"Auth Token: {data['token'][:10]}...")
            return data.get('token')
        
        elif response.status_code == 400:
            print(f"INFO: Registration failed (User likely exists).")
            print(f"Error Details: {json.dumps(data, indent=2)}")
        
        else:
            print(f"ERROR: Registration failed with status {response.status_code}")
            print(f"Response: {data}")
            
    except requests.exceptions.ConnectionError:
        print(f"FATAL ERROR: Could not connect to the server at {BASE_URL}. Ensure your Django server is running.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during registration: {e}")
        return None

def login_user():
    """Attempts to log in an existing user."""
    print("\n--- 2. Attempting to Log In User ---")
    login_data = {
        "email": TEST_USER["email"],
        "password": TEST_USER["password"]
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        data = response.json()

        if response.status_code == 200:
            print("SUCCESS: User logged in.")
            print(f"Auth Token: {data['token'][:10]}...")
            return data.get('token')
            
        else:
            print(f"ERROR: Login failed with status {response.status_code}")
            print(f"Error Details: {json.dumps(data, indent=2)}")
            return None

    except requests.exceptions.ConnectionError:
        print(f"FATAL ERROR: Could not connect to the server at {BASE_URL}. Ensure your Django server is running.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during login: {e}")
        return None

def main():
    token = register_user()
    if token:
        print("\nSuccessfully registered and received token.")
    
    login_token = login_user()
    if login_token:
        print("\nSuccessfully logged in and received token.")

if __name__ == "__main__":
    main()
