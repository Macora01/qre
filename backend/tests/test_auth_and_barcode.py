"""
Backend API Tests for QR Code Scanner App
Tests the new email-based authentication (no Google OAuth)
and barcode scanning functionality
"""

import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestHealthAndRoot:
    """Basic health check tests"""
    
    def test_api_root_endpoint(self):
        """Test API root returns ready message"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Ready" in data["message"]
        print("✅ API root endpoint working")


class TestEmailAuthentication:
    """Tests for email-based login (POST /api/auth/login)"""
    
    def test_login_with_valid_email(self):
        """Test login with valid email returns user data and sets session cookie"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": "test@example.com"},
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "user_id" in data, "Response should contain user_id"
        assert "email" in data, "Response should contain email"
        assert data["email"] == "test@example.com", "Email should match"
        assert "name" in data, "Response should contain name"
        
        # Check session cookie was set
        assert "session_token" in response.cookies, "Session cookie should be set"
        print(f"✅ Login with valid email works - user_id: {data['user_id']}")
        
        return response.cookies.get("session_token")
    
    def test_login_with_invalid_email_format(self):
        """Test login with invalid email returns 400 error"""
        invalid_emails = [
            "invalid",
            "invalid@",
            "@domain.com",
            "no-at-symbol",
            "spaces in@email.com",
            ""
        ]
        
        for invalid_email in invalid_emails:
            response = requests.post(
                f"{BASE_URL}/api/auth/login",
                json={"email": invalid_email},
                headers={"Content-Type": "application/json"}
            )
            
            # Should return 400 or 422 for validation error
            assert response.status_code in [400, 422], \
                f"Expected 400/422 for '{invalid_email}', got {response.status_code}"
        
        print("✅ Invalid email format returns 400 error")
    
    def test_login_email_case_insensitive(self):
        """Test that email is stored lowercase"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": "TEST_UPPERCASE@EXAMPLE.COM"},
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test_uppercase@example.com", "Email should be lowercase"
        print("✅ Email stored as lowercase")


class TestAuthenticatedEndpoints:
    """Tests for endpoints requiring authentication"""
    
    @pytest.fixture
    def auth_session(self):
        """Get authenticated session with cookies"""
        session = requests.Session()
        response = session.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": "testing_user@example.com"},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200, f"Login failed: {response.text}"
        return session
    
    def test_get_me_authenticated(self, auth_session):
        """Test GET /api/auth/me returns user data when authenticated"""
        response = auth_session.get(f"{BASE_URL}/api/auth/me")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "user_id" in data
        assert "email" in data
        assert data["email"] == "testing_user@example.com"
        print(f"✅ GET /api/auth/me works - email: {data['email']}")
    
    def test_get_me_unauthenticated(self):
        """Test GET /api/auth/me returns 401 when not authenticated"""
        response = requests.get(f"{BASE_URL}/api/auth/me")
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        print("✅ GET /api/auth/me returns 401 when unauthenticated")
    
    def test_logout(self, auth_session):
        """Test POST /api/auth/logout clears session"""
        # First verify we're authenticated
        me_response = auth_session.get(f"{BASE_URL}/api/auth/me")
        assert me_response.status_code == 200
        
        # Logout
        logout_response = auth_session.post(f"{BASE_URL}/api/auth/logout")
        assert logout_response.status_code == 200
        
        data = logout_response.json()
        assert "message" in data
        print("✅ POST /api/auth/logout works")
        
        # Verify session is cleared - should get 401 now
        me_after = auth_session.get(f"{BASE_URL}/api/auth/me")
        assert me_after.status_code == 401, "Session should be cleared after logout"
        print("✅ Session cleared after logout")


class TestBarcodeOperations:
    """Tests for barcode scanning endpoints"""
    
    @pytest.fixture
    def auth_session(self):
        """Get authenticated session"""
        session = requests.Session()
        response = session.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": "barcode_tester@example.com"},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
        return session
    
    def test_save_barcode_authenticated(self, auth_session):
        """Test POST /api/barcode saves barcode when authenticated"""
        test_barcode = "TEST_BARCODE_12345"
        
        response = auth_session.post(
            f"{BASE_URL}/api/barcode",
            json={"barcode": test_barcode},
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "barcode_count" in data
        assert "barcodes" in data
        assert "session_id" in data
        assert test_barcode in data["barcodes"], "Saved barcode should be in response"
        print(f"✅ Barcode saved - count: {data['barcode_count']}")
    
    def test_save_barcode_unauthenticated(self):
        """Test POST /api/barcode returns 401 when not authenticated"""
        response = requests.post(
            f"{BASE_URL}/api/barcode",
            json={"barcode": "UNAUTHORIZED_TEST"},
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 401
        print("✅ POST /api/barcode returns 401 when unauthenticated")
    
    def test_duplicate_barcode_detection(self, auth_session):
        """Test duplicate barcode is flagged but still saved"""
        test_barcode = "DUPLICATE_TEST_678"
        
        # First scan
        response1 = auth_session.post(
            f"{BASE_URL}/api/barcode",
            json={"barcode": test_barcode}
        )
        assert response1.status_code == 200
        data1 = response1.json()
        initial_count = data1["barcode_count"]
        
        # Second scan - same barcode (duplicate)
        response2 = auth_session.post(
            f"{BASE_URL}/api/barcode",
            json={"barcode": test_barcode}
        )
        assert response2.status_code == 200
        data2 = response2.json()
        
        assert data2["is_duplicate"] == True, "Should flag as duplicate"
        assert data2["barcode_count"] == initial_count + 1, "Count should still increase"
        print("✅ Duplicate barcode detection works")
    
    def test_get_session_stats(self, auth_session):
        """Test GET /api/session-stats returns session info"""
        response = auth_session.get(f"{BASE_URL}/api/session-stats")
        
        assert response.status_code == 200
        data = response.json()
        assert "barcode_count" in data
        assert "barcodes" in data
        assert "session_id" in data
        print(f"✅ Session stats - count: {data['barcode_count']}")


class TestFinalizeSession:
    """Tests for session finalization and CSV generation"""
    
    @pytest.fixture
    def auth_session_with_barcodes(self):
        """Get authenticated session and add some barcodes"""
        session = requests.Session()
        # Use unique email to get fresh session
        import uuid
        email = f"finalize_test_{uuid.uuid4().hex[:8]}@example.com"
        
        response = session.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": email}
        )
        assert response.status_code == 200
        
        # Add some barcodes
        for i in range(3):
            session.post(
                f"{BASE_URL}/api/barcode",
                json={"barcode": f"FINALIZE_TEST_{i}"}
            )
        
        return session
    
    def test_finalize_session_generates_csv(self, auth_session_with_barcodes):
        """Test POST /api/finalize-session generates CSV when authenticated"""
        response = auth_session_with_barcodes.post(f"{BASE_URL}/api/finalize-session")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "csv_filename" in data
        assert "barcode_count" in data
        assert data["barcode_count"] >= 3
        assert data["csv_filename"].endswith(".csv")
        print(f"✅ Session finalized - CSV: {data['csv_filename']}, count: {data['barcode_count']}")
    
    def test_finalize_session_unauthenticated(self):
        """Test POST /api/finalize-session returns 401 when not authenticated"""
        response = requests.post(f"{BASE_URL}/api/finalize-session")
        
        assert response.status_code == 401
        print("✅ POST /api/finalize-session returns 401 when unauthenticated")
    
    def test_finalize_empty_session_fails(self):
        """Test finalize with no barcodes returns error"""
        session = requests.Session()
        import uuid
        email = f"empty_session_{uuid.uuid4().hex[:8]}@example.com"
        
        # Login with new email (fresh session, no barcodes)
        response = session.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": email}
        )
        assert response.status_code == 200
        
        # Try to finalize empty session
        finalize_response = session.post(f"{BASE_URL}/api/finalize-session")
        
        # Should return 400 or 404 since no barcodes
        assert finalize_response.status_code in [400, 404], \
            f"Expected 400/404 for empty session, got {finalize_response.status_code}"
        print("✅ Finalize empty session correctly returns error")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
