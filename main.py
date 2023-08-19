from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/{owner}/{repo}")
def read_item(owner: str,repo: str, q: Union[str, None] = None):
    return {"owner": owner, "repo": repo, "q": q}
