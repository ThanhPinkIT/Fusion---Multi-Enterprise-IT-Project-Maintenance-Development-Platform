from database.models.tenant_user import TenantUser
from database.models.project_member import ProjectMember
from security.permission_map import ROLE_PERMISSIONS

def get_tenant_role(
    db,
    user_id: int,
    tenant_id: int | None
) -> str | None:
    """
    Lấy role của user trong tenant.
    Trả về None nếu user không thuộc tenant.
    """
    if tenant_id is None:
        return None

    tenant_user = (
        db.query(TenantUser)
        .filter(
            TenantUser.user_id == user_id,
            TenantUser.tenant_id == tenant_id
        )
        .first()
    )

    if tenant_user is None:
        return None

    return tenant_user.role


def get_project_role(
    db,
    user_id: int,
    project_id: int | None
) -> str | None:
    """
    Lấy role của user trong project.
    Trả về None nếu user không thuộc project.
    """
    if project_id is None:
        return None

    project_member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.user_id == user_id,
            ProjectMember.project_id == project_id
        )
        .first()
    )

    if project_member is None:
        return None

    return project_member.role

from security.permission_map import ROLE_PERMISSIONS

def resolve_permissions(
    db,
    user_id: int,
    tenant_id: int | None = None,
    project_id: int | None = None
) -> set[str]:
    """
    Gom toàn bộ permission của user dựa trên:
    - role trong tenant
    - role trong project
    """

    permissions: set[str] = set()

    tenant_role = get_tenant_role(db, user_id, tenant_id)
    if tenant_role:
        permissions |= ROLE_PERMISSIONS.get(tenant_role, set())

    project_role = get_project_role(db, user_id, project_id)
    if project_role:
        permissions |= ROLE_PERMISSIONS.get(project_role, set())

    return permissions
