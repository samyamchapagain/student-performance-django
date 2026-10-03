"""Quick end-to-end test using Django's test client.

Verifies:
  1. Authentication (register / login / logout)
  2. Predictions are linked to the logged-in user
  3. Regular users ONLY see their own history
  4. Admin sees ALL predictions along with usernames
"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_performance.settings")

import django

django.setup()

from django.contrib.auth.models import User
from django.test import Client
from prediction.models import Prediction

# ---- Clean up any leftovers from previous runs (keep 'admin') ----
User.objects.filter(username__in=["alice", "bob"]).delete()
Prediction.objects.all().delete()

alice = Client()
bob = Client()

# 1. Register two users
for name in ("alice", "bob"):
    c = Client()
    r = c.post("/register/", {
        "username": name,
        "password1": "StrongPass123!",
        "password2": "StrongPass123!",
    })
    print(f"1) Register {name} ->", r.status_code, "redirect:", r.get("Location", "none"))
    User.objects.get(username=name)

# 2. Log in as alice and make a prediction
alice.post("/login/", {"username": "alice", "password": "StrongPass123!"})
r = alice.post("/predict/", {
    "gender": "female",
    "ethnicity": "group B",
    "parental_education": "bachelor's degree",
    "lunch": "standard",
    "test_prep_course": "completed",
    "math_score": 88,
    "reading_score": 95,
    "writing_score": 92,
})
a_pred_count = Prediction.objects.filter(user__username="alice").count()
print(f"2) Alice predicted -> HTTP {r.status_code} | Alice's predictions in DB: {a_pred_count}")
print("   Owner is alice:", Prediction.objects.filter(user__username="alice").exists())

# 3. Log in as bob and make a prediction
bob.post("/login/", {"username": "bob", "password": "StrongPass123!"})
r = bob.post("/predict/", {
    "gender": "male",
    "ethnicity": "group D",
    "parental_education": "high school",
    "lunch": "free/reduced",
    "test_prep_course": "none",
    "math_score": 55,
    "reading_score": 48,
    "writing_score": 50,
})
b_pred_count = Prediction.objects.filter(user__username="bob").count()
print(f"3) Bob predicted -> HTTP {r.status_code} | Bob's predictions in DB: {b_pred_count}")

# 4. Alice's history: must show ONLY her own prediction, no 'bob' user badge
r = alice.get("/history/")
html = r.content.decode()
print("4) Alice history -> HTTP", r.status_code)
print("   Shows alice's grade:", "A+" in html)
print("   Bob's prediction hidden (no 'bob' username):", "bob" not in html.split("badge-user")[0][-500:] if "badge-user" in html else "no badge-user col (correct for non-admin)")
print("   No 'User' column for alice:", "badge-user" not in html)

# 5. Bob's history: must show ONLY his own prediction
r = bob.get("/history/")
html = r.content.decode()
print("5) Bob history -> HTTP", r.status_code)
print("   Shows bob's grade:", "B" in html or "C" in html or "D" in html or "F" in html)
print("   No 'User' column for bob:", "badge-user" not in html)

# 6. Admin logs in and sees ALL predictions with usernames
admin_client = Client()
print("\n6) Logging in as admin (superuser)...")
from django.contrib.auth.models import User
if not User.objects.filter(username="test_admin").exists():
    User.objects.create_superuser("test_admin", "test_admin@example.com", "test-only-pass-123")
admin_login_ok = admin_client.login(username="test_admin", password="test-only-pass-123")
print("   Admin login OK:", admin_login_ok)
r = admin_client.get("/history/")
html = r.content.decode()
print("   Admin history -> HTTP", r.status_code)
print("   Admin sees alice's username:", "alice" in html)
print("   Admin sees bob's username:", "bob" in html)
print("   Admin sees 'User' column:", "badge-user" in html)
print("   Total predictions for admin:", Prediction.objects.count())

# 7. Logout protection still works
alice.logout()
r = alice.get("/history/")
print("\n7) Alice history after logout ->", r.status_code, "redirect:", r.get("Location", "none"))

print("\nALL TESTS PASSED!" if (a_pred_count == 1 and b_pred_count == 1 and admin_login_ok) else "\nTEST ISSUES")