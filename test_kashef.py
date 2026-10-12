import os
import unittest
import json
from app import app, db, User, Medicine, AnalysisHistory, Feedback, AuditLog

class KashefTestSuite(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            from app import seed_database
            seed_database()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_public_pages(self):
        """Test public endpoints are accessible without authentication."""
        for path in ["/", "/help", "/privacy", "/terms", "/login", "/register", "/forgot-password", "/feedback"]:
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, 200, f"Route {path} failed with {resp.status_code}")

    def test_bilingual_switching(self):
        """Test language toggle switches session and layout direction."""
        resp = self.client.get("/set-lang/en", follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'dir="ltr"', resp.data)

        resp = self.client.get("/set-lang/ar", follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'dir="rtl"', resp.data)

    def test_user_authentication_and_isolation(self):
        """Test login, dashboard, and role permissions."""
        # 1. Login as standard user
        login_resp = self.client.post("/login", data={
            "email": "user@kashef.com",
            "password": "User@123"
        }, follow_redirects=True)
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn("Mohammed Ali", login_resp.data.decode("utf-8"))

        # 2. Regular user should be forbidden from admin area
        admin_resp = self.client.get("/admin", follow_redirects=True)
        self.assertIn("dashboard", admin_resp.request.path)

        # 3. Create a sample scan
        sample_resp = self.client.get("/sample-scan/paracetamol", follow_redirects=True)
        self.assertEqual(sample_resp.status_code, 200)
        self.assertIn("Paracetamol", sample_resp.data.decode("utf-8"))

    def test_admin_rbac_and_modules(self):
        """Test admin login, sidebar endpoints, and role management."""
        # Login as Admin
        self.client.post("/login", data={
            "email": "admin@kashef.com",
            "password": "Admin@123"
        }, follow_redirects=True)

        # Check all admin endpoints
        for path in ["/admin", "/admin/users", "/admin/medicines", "/admin/history", "/admin/feedback", "/admin/settings", "/admin/audit-log"]:
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, 200, f"Admin route {path} returned {resp.status_code}")

        # Check modifying role of standard user
        with app.app_context():
            u = User.query.filter_by(email="user@kashef.com").first()
            user_id = u.id

        role_resp = self.client.post(f"/admin/users/{user_id}/role", data={"role": "pharmacist"}, follow_redirects=True)
        self.assertEqual(role_resp.status_code, 200)

        with app.app_context():
            u = db.session.get(User, user_id)
            self.assertEqual(u.role, "pharmacist")

    def test_pharmacist_portal(self):
        """Test pharmacist can access reviews portal."""
        self.client.post("/login", data={
            "email": "pharmacist@kashef.com",
            "password": "Pharma@123"
        }, follow_redirects=True)

        resp = self.client.get("/pharmacist/reviews")
        self.assertEqual(resp.status_code, 200)

    def test_ai_analyzer_extraction(self):
        """Test medicine analysis service entity extraction."""
        from services.ai_service import analyze_text
        text = (
            "Panadol Advance 500 mg Tablets\n"
            "الجرعة: قرص إلى قرصين كل 4 إلى 6 ساعات عند اللزوم.\n"
            "تحذير: لا تتناول أكثر من 8 أقراص خلال 24 ساعة.\n"
            "الاحتياطات: استشر الطبيب في حال الحمل أو أمراض الكبد.\n"
            "يحفظ في مكان جاف أقل من 25 درجة مئوية."
        )
        res = analyze_text(text)
        self.assertTrue(res["found_any"])
        self.assertIn("500", res["name"])
        self.assertTrue(len(res["warnings"]) > 0)
        self.assertTrue(len(res["precautions"]) > 0)
        self.assertTrue(res["completeness"] > 50)

if __name__ == "__main__":
    unittest.main()
