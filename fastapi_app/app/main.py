"""
Main FASTAPI module
"""

import uvicorn
from models import build_schema, Url, session as s
from schema import Url as SchemaUrl
from celery import Celery

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.post("/urls")
def load_url(url: SchemaUrl) -> dict:
    """
    Post new url to a database by Celery task
    :param url: JSON object checking by pydantic class
    :return: {"id": <id of created Url in DB>}
    """
    celery_app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis')
    result = celery_app.send_task('tasks.add_url', [url.url])
    return result.get()


@app.get("/urls/{url_id}")
def get_single_url(url_id: int) -> dict:
    """
    Get the processed url from the DB
    :param url_id:
    :return: dict as {
        'id': <id of Url>,
        'url': <url to file>,
        'processed': <boolean status of processed>,
        'error': <error text if any>}
    }
    """
    url = s.query(Url).filter(Url.id == url_id).first()

    if not url:
        raise HTTPException(status_code=404, detail=f"Url with id={url_id} not found")

    return url.as_dict


@app.get("/urls")
def get_urls() -> list:
    """
    Get all urls in the DB
    :return: list of url with the following schema:
        {
            'id': <id of Url>,
            'url': <url to file>,
            'processed': <boolean status of processed>,
            'error': <error text if any>}
        }
    """
    return [url.as_dict for url in s.query(Url).order_by(Url.id)]


@app.get("/keys/{url_id}")
def get_single_key(url_id: int):
    """
    Get the key by specified url_id
    :param url_id:
    :return: dict as {
        'id': <id of Url>,
        'url': <url to file>,
        'keys': [list of stored keys from a XML-file]
    }

    """
    key = s.query(Url).filter(Url.id == url_id).first()

    if not key:
        raise HTTPException(status_code=404, detail=f"Key with url_id={url_id} not found")

    return key.as_dict_with_keys


@app.get("/keys")
def get_keys():
    """
    Get all urls with keys inside
    :return: a list with a keys by the following schema:
    {
        'id': <id of Url>,
        'url': <url to file>,
        'keys': [list of stored keys from a XML-file]
    }
    """
    return [url.as_dict_with_keys for url in s.query(Url).order_by(Url.id)]


if __name__ == "__main__":
    build_schema()
    uvicorn.run(app, host="0.0.0.0", port=8000)
