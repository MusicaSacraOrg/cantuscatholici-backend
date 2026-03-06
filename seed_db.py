from pydantic import SecretStr

from app.database import SessionLocal
from app.user.auth import get_password_hash
from app.user.models import User
from app.user_role.models import UserRole

USERS_TO_CREATE = [
    {
        "name": "Admin",
        "surname": "Admin",
        "email": "admin@admin.com",
        "password": "Admin1234-",
        "role": "Admin",
    },
]

def seed_users():
    session = SessionLocal()

    try:
        for user in USERS_TO_CREATE:
            role = session.query(UserRole).filter(UserRole.role == user["role"]).first()
            if not role:
                print(f"!! Role {user['role']} not found — skipping user")
                continue

            new_user = User(
                email=user["email"],
                hashed_password=get_password_hash(SecretStr(user["password"])),
                role_id=role.id,
            )
            session.add(new_user)
            session.commit()
            print(f"✅ Created user: {user['email']} with role {user['role']}")

    finally:
        session.close()


if __name__ == "__main__":
    seed_users()
    print("Done.")
