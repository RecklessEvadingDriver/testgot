"""
Simple example client for WromGPT API
Demonstrates how to interact with the API endpoints
"""

import requests
import json

# Configuration
API_BASE_URL = "http://localhost:8000"


def test_health():
    """Test the health check endpoint"""
    print("\n=== Testing Health Check ===")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_root():
    """Test the root endpoint"""
    print("\n=== Testing Root Endpoint ===")
    response = requests.get(f"{API_BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_chat(message, max_length=100, temperature=0.7, custom_instructions=None):
    """Test the chat endpoint"""
    print(f"\n=== Testing Chat: '{message}' ===")
    
    payload = {
        "message": message,
        "max_length": max_length,
        "temperature": temperature
    }
    
    if custom_instructions:
        payload["custom_instructions"] = custom_instructions
    
    response = requests.post(
        f"{API_BASE_URL}/api/chat",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Model Used: {data['model_used']}")
        print(f"Response: {data['response']}")
    else:
        print(f"Error: {response.text}")


def test_get_instructions():
    """Test getting current instructions"""
    print("\n=== Testing Get Instructions ===")
    response = requests.get(f"{API_BASE_URL}/api/instructions")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_update_instructions(new_instructions):
    """Test updating instructions"""
    print("\n=== Testing Update Instructions ===")
    response = requests.post(
        f"{API_BASE_URL}/api/instructions",
        json={"instructions": new_instructions},
        headers={"Content-Type": "application/json"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def main():
    """Run all tests"""
    print("=" * 60)
    print("WromGPT API Client - Testing Suite")
    print("=" * 60)
    
    try:
        # Test basic endpoints
        test_root()
        test_health()
        
        # Test getting current instructions
        test_get_instructions()
        
        # Test chat with default instructions
        test_chat("Hello! What is your purpose?", max_length=150)
        
        # Test chat with custom instructions
        test_chat(
            "What is Python?",
            max_length=150,
            custom_instructions="You are a Python programming expert. Be concise and technical."
        )
        
        # Test updating system instructions
        test_update_instructions(
            "You are WromGPT, a friendly AI assistant specializing in technology and science."
        )
        
        # Test chat with updated instructions
        test_chat("Tell me about machine learning", max_length=150)
        
        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API.")
        print(f"Please make sure the server is running at {API_BASE_URL}")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")


if __name__ == "__main__":
    main()
