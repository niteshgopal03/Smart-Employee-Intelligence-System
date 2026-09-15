from fastapi import Depends, HTTPException

from security.auth_dependency import get_current_user


def require_role(*roles):

    allowed_roles = {
        str(role).strip().lower()
        for role in roles
    }

    def role_dependency(
        current_user=Depends(get_current_user)
    ):

        user_role = str(
            current_user.get("role", "")
        ).strip().lower()

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail={
                    "message": "Access Denied",
                    "jwt_role": current_user.get("role"),
                    "allowed_roles": list(allowed_roles)
                }
            )

        return current_user

    return role_dependency