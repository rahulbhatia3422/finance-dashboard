from fastapi import Header, HTTPException

def check_role(allowed_roles: list):
    def role_dependency(role: str = Header(...)):
        if role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access Denied")
        return role
    return role_dependency