from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from security.deps import get_current_user
from security.permission_utils import resolve_permissions


def require_permission(permission_code: str):
    def checker(
        tenant_id: int | None = None,
        project_id: int | None = None,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        # ✅ SYSTEM ADMIN BYPASS
        if getattr(current_user, "is_system_admin", False):
            return current_user

        permissions = resolve_permissions(
            db=db,
            user_id=current_user.id,
            tenant_id=tenant_id,
            project_id=project_id
        )

        if permission_code not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền thực hiện hành động này"
            )

        return current_user

    return checker
