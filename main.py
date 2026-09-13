from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import sqlite3
from pathlib import Path

app = FastAPI(title="Task API")

DB_PATH = Path(__file__).resolve().parent / "tasks.db"


class TaskCreate(BaseModel):
    title: str
    done: bool = False


class TaskUpdate(BaseModel):
    title: str
    done: bool


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)

    count = conn.execute("SELECT COUNT(*) AS count FROM tasks").fetchone()["count"]

    if count == 0:
        conn.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Learn FastAPI", 0),
                ("Connect FastAPI to SQLite", 0),
                ("Test the CRUD API", 0),
            ],
        )

    conn.commit()
    conn.close()


@app.on_event("startup")
def startup():
    initialize_database()


@app.get("/")
def home():
    return {"message": "Hello from my Task API"}


@app.get("/tasks")
def get_tasks():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, title, done FROM tasks ORDER BY id"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_connection()
    row = conn.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,),
    ).fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return dict(row)


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")

    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title.strip(), int(task.done)),
    )
    task_id = cursor.lastrowid
    conn.commit()

    row = conn.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,),
    ).fetchone()
    conn.close()

    return dict(row)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")

    conn = get_connection()
    cursor = conn.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (task.title.strip(), int(task.done), task_id),
    )

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    conn.commit()
    row = conn.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,),
    ).fetchone()
    conn.close()

    return dict(row)


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    conn = get_connection()
    cursor = conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,),
    )

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    conn.commit()
    conn.close()
    return Response(status_code=204)
