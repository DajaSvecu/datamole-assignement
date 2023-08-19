import os
from typing import Union
from src.event_count import get_events_count

from fastapi import FastAPI

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise EnvironmentError("Api Token not found!")

HEADERS = {
    "Accept":"application/vnd.github+json",
    "Authorization":"Bearer {}".format(API_TOKEN)
}

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/events_count/{off_set}")
def events_count(off_set: int):
    return get_events_count(off_set,HEADERS)


@app.get("/avg_pull_request/{owner}/{repo}")
def avg_pull_request(owner: str,repo: str, q: Union[str, None] = None):
    return {"owner": owner, "repo": repo, "q": q}
