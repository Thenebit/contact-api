# Contact API

Practice project — Dockerized FastAPI + SQLModel + PostgreSQL CRUD.

## Stack

- **API:** FastAPI + SQLModel (Python 3.12)
- **DB:** PostgreSQL 16
- **Containerized:** Docker Compose

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/contact-api.git
cd contact-api
```

Create `.env`:

```
POSTGRES_USER=contact
POSTGRES_PASSWORD=contact_dev_pw
POSTGRES_DB=contact_db
DB_HOST=db
DB_PORT=5432
```

Run:

```bash
docker compose up --build
```

## Usage

- **API docs:** http://localhost:8000/docs
- **Health check:** http://localhost:8000/health

## Endpoints

| Method | Path                    | Description        |
|--------|-------------------------|--------------------|
| POST   | `/messages`             | Create a message   |
| GET    | `/messages`             | List all messages  |
| GET    | `/messages/{message_id}`| Get one message    |
| DELETE | `/messages/{message_id}`| Delete a message   |

## Tests

```bash
docker compose exec api python -m pytest app/tests -v --rootdir /code
```
