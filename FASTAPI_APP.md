# FAST API Application

## Docs

[Official FastAPI deployment](https://fastapi.tiangolo.com/deployment/)
[TestDriven](https://testdriven.io/courses/tdd-fastapi/docker-config/)
[SQLAlchemy](https://docs.sqlalchemy.org/en/13/)
[alembic for SQLAlchemy migration](https://alembic.sqlalchemy.org/en/latest/)
[Full Stack FastAPI and PostgreSQL - Base Project Generator](https://github.com/tiangolo/full-stack-fastapi-postgresql)
[Docker development](https://www.docker.com/blog/containerized-python-development-part-3/)

## Setup 

```shell script
mkdir fastapi_app
cd fastapi_app
vim Dockerfile
```

```dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app
```

```shell script
mkdir app
cd app
vim main.py
```

```python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

```shell script
cd ..

docker build -t fastapi_app .
docker run -d --name fastapi_app -p 80:80 fastapi_app
```

