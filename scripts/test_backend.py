"""
Test script to verify backend API is working
"""
import requests
import sys

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            print("✓ Health endpoint is working")
            print(f"  Response: {response.json()}")
            return True
        else:
            print(f"✗ Health endpoint returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to backend. Is it running?")
        return False
    except Exception as e:
        print(f"✗ Error testing health endpoint: {e}")
        return False

def test_classes_endpoint():
    """Test the classes endpoint"""
    try:
        response = requests.get('http://localhost:5000/classes', timeout=5)
        if response.status_code == 200:
            print("✓ Classes endpoint is working")
            data = response.json()
            print(f"  Total classes: {data.get('total', 0)}")
            return True
        else:
            print(f"✗ Classes endpoint returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error testing classes endpoint: {e}")
        return False

def main():
    print("Testing Plant Disease Detection Backend API")
    print("=" * 50)
    
    health_ok = test_health_endpoint()
    classes_ok = test_classes_endpoint()
    
    print("=" * 50)
    if health_ok and classes_ok:
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print("✗ Some tests failed")
        sys.exit(1)

if __name__ == '__main__':
    main()
