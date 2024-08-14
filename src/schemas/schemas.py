from pydantic import BaseModel


class Root200(BaseModel):
    message: str = "Hello World!"
