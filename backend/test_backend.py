import requests
import json

def test_backend():
    """Test that the backend is running properly"""
    try:
        # Test if the server is running
        response = requests.get("http://localhost:8000/docs", timeout=5)
        
        if response.status_code == 200:
            print("✅ Backend is running successfully!")
            print(f"✅ API Documentation available at http://localhost:8000/docs")
            print(f"✅ Status code: {response.status_code}")
            
            # Also check the main API root
            try:
                root_response = requests.get("http://localhost:8000/api/v1", timeout=5)
                print(f"✅ API Root accessible, status: {root_response.status_code}")
            except:
                print("⚠️  API Root not accessible, but documentation is available")
                
        else:
            print(f"❌ Backend responded with status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8000")
    except requests.exceptions.Timeout:
        print("❌ Connection timed out. Backend might not be responding.")
    except Exception as e:
        print(f"❌ Error testing backend: {str(e)}")

if __name__ == "__main__":
    print("Testing backend connectivity...")
    test_backend()