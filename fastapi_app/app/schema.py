"""
Just one example of usage pydantic models
"""

from pydantic import BaseModel, AnyHttpUrl


class Url(BaseModel):
    url: AnyHttpUrl
