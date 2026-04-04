from fastapi import HTTPException, Depends
from app.utils.auth import verify_token

def check_role(allowed_roles: list):
    def role_dependency(payload=Depends(verify_token)):
        role = payload.get("role")

        if role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access Denied")

        return role
    return role_dependency