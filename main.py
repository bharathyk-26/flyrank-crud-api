from pydantic import BaseModel

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):

    for task in tasks:
        if task["id"] == task_id:

            if task_update.title is None and task_update.done is None:
                raise HTTPException(
                    status_code=400,
                    detail="At least one field is required"
                )

            if task_update.title is not None:
                if not task_update.title.strip():
                    raise HTTPException(
                        status_code=400,
                        detail="Title cannot be empty"
                    )
                task["title"] = task_update.title

            if task_update.done is not None:
                task["done"] = task_update.done

            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )