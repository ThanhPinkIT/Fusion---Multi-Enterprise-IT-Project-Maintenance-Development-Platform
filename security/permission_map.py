ROLE_PERMISSIONS = {
    # ===== TENANT LEVEL =====
    "TENANT_ADMIN": {
        "tenant.user.invite",
        "tenant.user.remove",
        "tenant.project.create",
        "tenant.view_all",

        # tenant admin làm được mọi thứ trong project
        "project.view",
        "project.task.view",
        "project.task.create",
        "project.task.update",
        "project.task.delete",
        "project.task.assign",
    },

    # ===== PROJECT / TENANT ROLES =====
    "PM": {
        "tenant.project.create",

        "project.view",
        "project.task.view",
        "project.task.create",
        "project.task.update",
        "project.task.delete",
        "project.task.assign",
    },

    "BA": {
        "project.view",
        "project.task.view",
        "project.task.create",
        "project.task.update",
        "project.customer.comment",
    },

    "DEV": {
        "project.view",
        "project.task.view",
        "project.task.update",
    },

    "CUSTOMER": {
        "project.view",
        "project.task.view",
        "project.customer.comment",
    },
}
