# FlyRank W3 A2 — Task CRUD API with SQLite

This project completes FlyRank Week 3 Assignment A2 by moving the Task API
storage from an in-memory list to a real SQLite database.

## Architecture

Client → FastAPI → SQLite (`tasks.db`)

The API endpoints remain the same while the storage layer changes.

## Technologies

- Python 3.10+
- FastAPI
- Uvicorn
- SQLite (`sqlite3`, Python standard library)

## Why SQLite?

SQLite was chosen because it is a lightweight database stored in a single file,
requires no separate database server, needs zero database setup, and provides
persistence across server restarts.

## Database

The database file is `tasks.db` in the project folder. The application creates
it automatically when the server starts. The `tasks` table is also created
automatically if it is missing.

Columns:

- `id` — integer primary key
- `title` — text
- `done` — boolean stored by SQLite as 0/1

Three example tasks are inserted only when the table is empty, so restarting
the server does not duplicate the seed data.

## Run the project

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open:

- API: http://127.0.0.1:8000/
- Swagger/OpenAPI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## CRUD endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/tasks` | List all tasks |
| GET | `/tasks/{id}` | Get one task |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

## Example curl tests

List tasks:

```bash
curl -i http://127.0.0.1:8000/tasks
```

Get one task:

```bash
curl -i http://127.0.0.1:8000/tasks/1
```

Create:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks   -H "Content-Type: application/json"   -d '{"title":"Finish FlyRank assignment","done":false}'
```

Update:

```bash
curl -i -X PUT http://127.0.0.1:8000/tasks/1   -H "Content-Type: application/json"   -d '{"title":"Learn FastAPI and SQLite","done":true}'
```

Delete:

```bash
curl -i -X DELETE http://127.0.0.1:8000/tasks/1
```

Unknown ID should return 404:

```bash
curl -i http://127.0.0.1:8000/tasks/999
```

## Parameterized SQL

User-controlled values are passed separately using `?` placeholders, for example:

```python
conn.execute(
    "SELECT id, title, done FROM tasks WHERE id = ?",
    (task_id,),
)
```

This avoids constructing SQL by directly concatenating user input.

## Stage 4 SQL example

```sql
SELECT * FROM tasks WHERE done = 1;
```

This returns only completed tasks.

## Persistence proof

Create a task with POST, stop the server with `Ctrl+C`, start it again, and run:

```bash
curl -i http://127.0.0.1:8000/tasks
```

The created task remains because it is stored in `tasks.db`.

## Submission checklist

- [x] SQLite database
- [x] `tasks` table created automatically
- [x] Three seed tasks only when table is empty
- [x] GET all
- [x] GET one
- [x] POST
- [x] PUT
- [x] DELETE
- [x] Parameterized queries
- [x] 200 / 201 / 204 / 400 / 404 behavior
- [x] README
- [x] DB Browser screenshot included as `db_browser_screenshot.png`

## GitHub

Use the same public repository from Assignment 1, as required by the
assignment. Commit each stage separately and push the repository publicly.

Suggested commit messages:

1. `Stage 0: create SQLite database`
2. `Stage 1: database read endpoints`
3. `Stage 2: insert into database`
4. `Stage 3: update and delete with SQL`
5. `Stage 4: explored SQLite`
6. `Stage 5: database documentation`
