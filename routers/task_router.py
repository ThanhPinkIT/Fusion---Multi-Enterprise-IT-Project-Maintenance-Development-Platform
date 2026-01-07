from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from security.permissions import require_permission
import repositories.task_repository as repo

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["Tasks"])


# =====================
# GET ALL TASKS IN PROJECT
# =====================
@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("project.task.view"))
):
    return repo.get_tasks_by_project(db, project_id)


# =====================
# GET SINGLE TASK
# =====================
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("project.task.view"))
):
    task = repo.get_task_by_id(db, task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# =====================
# CREATE TASK
# =====================
@router.post("/", response_model=TaskResponse)
def create_task(
    project_id: int,
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("project.task.create"))
):
    return repo.create_task(
        db=db,
        data=data,
        project_id=project_id,
        creator_id=current_user.id
    )


# =====================
# UPDATE TASK
# =====================
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    project_id: int,
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("project.task.update"))
):
    task = repo.get_task_by_id(db, task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")

    return repo.update_task(db, task_id, data)


# =====================
# DELETE TASK
# =====================
@router.delete("/{task_id}")
def delete_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("project.task.delete"))
):
    success = repo.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Deleted successfully"}
