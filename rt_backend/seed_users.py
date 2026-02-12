"""
Seed script to create demo users in the database.
Run: python seed_users.py
"""
import sys
import os

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from passlib.context import CryptContext
from app.db.session import SessionLocal
from app.db import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DEMO_USERS = [
    {
        "email": "admin@demo.com",
        "password": "admin123",
        "full_name": "Admin User",
        "is_active": True,
        "is_superuser": True,
    },
    {
        "email": "recruiter@demo.com",
        "password": "recruiter123",
        "full_name": "Demo Recruiter",
        "is_active": True,
        "is_superuser": False,
    },
]


def seed_users():
    db = SessionLocal()
    try:
        for user_data in DEMO_USERS:
            existing = db.query(models.User).filter(
                models.User.email == user_data["email"]
            ).first()

            if existing:
                print(f"  ⏭  User '{user_data['email']}' already exists, skipping.")
                continue

            user = models.User(
                email=user_data["email"],
                hashed_password=pwd_context.hash(user_data["password"]),
                full_name=user_data["full_name"],
                is_active=user_data["is_active"],
                is_superuser=user_data["is_superuser"],
            )
            db.add(user)
            print(f"  ✅ Created user '{user_data['email']}' (password: {user_data['password']})")

        db.commit()
        print("\nDone! Demo users seeded successfully.")
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error seeding users: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Seeding demo users...\n")
    seed_users()
