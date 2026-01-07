from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.project_schema import ProjectCreate, ProjectUpdate, ProjectResponse
import repositories.project_repository as repo
from security.permissions import require_permission

router = APIRouter(prefix="/projects", tags=["Projects"])

# VIEW PROJECTS

@router.get("/", response_model=list[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("project.view"))
):
    return repo.get_all_projects(db)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("project.view"))
):
    project = repo.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


# CREATE PROJECT

@router.post("/", response_model=ProjectResponse)
def create_project(
    tenant_id: int,
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("tenant.project.create"))
):
    return repo.create_project(
        db,
        data,
        owner_id=current_user.id,
        tenant_id=tenant_id
    )

# UPDATE PROJECT

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("project.update"))
):
    project = repo.update_project(db, project_id, data)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


# DELETE PROJECT

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("project.delete"))
):
    success = repo.delete_project(db, project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Deleted successfully"}
