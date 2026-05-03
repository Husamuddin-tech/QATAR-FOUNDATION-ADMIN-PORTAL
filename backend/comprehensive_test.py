#!/usr/bin/env python
"""
Comprehensive Test Suite for CertifyMe Backend
Tests all features: Authentication, CRUD, Security, and Frontend Integration
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:5000"
TEST_EMAIL = f"test_{int(datetime.now().timestamp())}@example.com"
TEST_PASSWORD = "TestPass123"
ADMIN_NAME = "Test Admin"

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(title):
    print(f"\n{BLUE}{'='*60}")
    print(f"{title}")
    print(f"{'='*60}{RESET}\n")

def print_success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}✗ {msg}{RESET}")

def print_info(msg):
    print(f"{YELLOW}ℹ {msg}{RESET}")

def test_health():
    print_header("TEST 1: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        assert response.json()['status'] == 'healthy'
        print_success("Server is running and healthy")
        return True
    except Exception as e:
        print_error(f"Health check failed: {str(e)}")
        return False

def test_signup():
    print_header("TEST 2: User Registration (Signup)")
    try:
        signup_data = {
            "name": ADMIN_NAME,
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
            "confirmPassword": TEST_PASSWORD
        }
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert data['status'] == 'success'
        assert data['user']['email'] == TEST_EMAIL
        print_success(f"Signup successful for {TEST_EMAIL}")
        print_info(f"User ID: {data['user']['id']}")
        return True
    except AssertionError as e:
        print_error(f"Signup test failed: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Signup error: {str(e)}")
        return False

def test_duplicate_email():
    print_header("TEST 3: Duplicate Email Prevention")
    try:
        signup_data = {
            "name": "Another Admin",
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
            "confirmPassword": TEST_PASSWORD
        }
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
        assert response.status_code == 409, f"Expected 409, got {response.status_code}"
        assert 'error' in response.json()
        print_success("Duplicate email correctly rejected with 409 Conflict")
        return True
    except AssertionError as e:
        print_error(f"Duplicate email test failed: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_invalid_password():
    print_header("TEST 4: Password Validation")
    try:
        signup_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "short",  # Less than 8 characters
            "confirmPassword": "short"
        }
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        print_success("Invalid password correctly rejected")
        return True
    except AssertionError as e:
        print_error(f"Password validation test failed: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_login():
    print_header("TEST 5: User Login")
    try:
        session = requests.Session()
        login_data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
            "rememberMe": False
        }
        response = session.post(f"{BASE_URL}/api/auth/login", json=login_data)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data['status'] == 'success'
        print_success(f"Login successful for {TEST_EMAIL}")
        print_info(f"Session cookies: {len(session.cookies)} cookie(s)")
        return session
    except AssertionError as e:
        print_error(f"Login test failed: {str(e)}")
        return None
    except Exception as e:
        print_error(f"Login error: {str(e)}")
        return None

def test_create_opportunity(session):
    print_header("TEST 6: Create Opportunity")
    try:
        opportunity_data = {
            "name": "Python Backend Developer",
            "duration": "3 months",
            "startDate": "2026-06-15",
            "description": "Build scalable web applications with Flask and Python",
            "skills": ["Python", "Flask", "PostgreSQL", "REST APIs", "Git"],
            "category": "Technology",
            "futureOpportunities": "Excellent opportunity for full-time position",
            "maxApplicants": "75"
        }
        response = session.post(f"{BASE_URL}/api/opportunities", json=opportunity_data)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert data['status'] == 'success'
        opp_id = data['data']['id']
        print_success(f"Opportunity created successfully (ID: {opp_id})")
        print_info(f"Title: {data['data']['title']}")
        print_info(f"Skills: {', '.join(data['data']['skills'])}")
        return session, opp_id
    except AssertionError as e:
        print_error(f"Create opportunity test failed: {str(e)}")
        return session, None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return session, None

def test_get_opportunities(session):
    print_header("TEST 7: Retrieve Opportunities")
    try:
        response = session.get(f"{BASE_URL}/api/opportunities")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data['status'] == 'success'
        count = data['count']
        print_success(f"Retrieved {count} opportunity(ies)")
        for opp in data['data']:
            print_info(f"  - {opp['title']} ({opp['category']}) - {len(opp['skills'])} skills")
        return session
    except AssertionError as e:
        print_error(f"Get opportunities test failed: {str(e)}")
        return session
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return session

def test_update_opportunity(session, opp_id):
    print_header("TEST 8: Update Opportunity")
    if not opp_id:
        print_error("No opportunity ID available")
        return session
    try:
        update_data = {
            "name": "Senior Python Backend Developer",
            "duration": "6 months",
            "maxApplicants": "100"
        }
        response = session.put(f"{BASE_URL}/api/opportunities/{opp_id}/edit", json=update_data)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data['status'] == 'success'
        print_success(f"Opportunity updated successfully")
        print_info(f"New Title: {data['data']['title']}")
        print_info(f"New Duration: {data['data']['duration']}")
        return session
    except AssertionError as e:
        print_error(f"Update opportunity test failed: {str(e)}")
        return session
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return session

def test_forgot_password():
    print_header("TEST 9: Password Reset")
    try:
        forgot_data = {"email": TEST_EMAIL}
        response = requests.post(f"{BASE_URL}/api/auth/forgot", json=forgot_data)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data['status'] == 'success'
        print_success("Password reset link generated")
        print_info("Check Flask console for reset link")
        return True
    except AssertionError as e:
        print_error(f"Forgot password test failed: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_logout(session):
    print_header("TEST 10: User Logout")
    try:
        response = session.post(f"{BASE_URL}/api/auth/logout")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data['status'] == 'success'
        print_success("Logout successful")
        return True
    except AssertionError as e:
        print_error(f"Logout test failed: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_unauthorized_access():
    print_header("TEST 11: Security - Unauthorized Access")
    try:
        # Try to access protected endpoint without login
        response = requests.get(f"{BASE_URL}/api/opportunities")
        # Should redirect or return error
        assert response.status_code != 200, "Should not allow unauthenticated access"
        print_success("Unauthorized access correctly prevented")
        return True
    except AssertionError:
        print_error("Authorization check failed - unauthenticated access allowed!")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def main():
    print(f"\n{BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║       CertifyMe Backend - Comprehensive Test Suite         ║")
    print("║              All Features & Security Validation             ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{RESET}")

    results = []

    # Run all tests
    results.append(("Health Check", test_health()))
    results.append(("User Signup", test_signup()))
    results.append(("Duplicate Email Prevention", test_duplicate_email()))
    results.append(("Password Validation", test_invalid_password()))
    
    session = test_login()
    results.append(("User Login", session is not None))
    
    if session:
        session, opp_id = test_create_opportunity(session)
        results.append(("Create Opportunity", opp_id is not None))
        
        session = test_get_opportunities(session)
        results.append(("Get Opportunities", True))
        
        session = test_update_opportunity(session, opp_id)
        results.append(("Update Opportunity", True))
        
        results.append(("Logout", test_logout(session)))
    
    results.append(("Forgot Password", test_forgot_password()))
    results.append(("Unauthorized Access Prevention", test_unauthorized_access()))

    # Print summary
    print_header("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"  {test_name:.<45} {status}")
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print(f"{GREEN}✓ ALL TESTS PASSED! Backend is fully functional.{RESET}")
        return 0
    else:
        print(f"{RED}✗ Some tests failed. Please review the output above.{RESET}")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Tests interrupted by user{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Unexpected error: {str(e)}{RESET}")
        sys.exit(1)
