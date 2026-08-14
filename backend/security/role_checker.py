from fastapi import Depends, HTTPException

from security.auth_dependency import get_current_user


def require_role(*roles):

    def role_dependency(current_user=Depends(get_current_user)):

        if current_user["role"] not in roles:

            raise HTTPException(
                status_code=403,
                detail="Access Denied"
            )

        return current_user

    return role_dependency