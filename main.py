import os
from fastapi import FastAPI
from src import get_avg_time_between_repo_events, get_events_count

EVENT_TYPES = ("WatchEvent","PullRequestEvent","IssuesEvent")
PULL_REQUEST_EVENT = "PullRequestEvent"

HEADERS = {
    "Accept":"application/vnd.github+json",
}
API_TOKEN = os.getenv("API_TOKEN")
if API_TOKEN:
    HEADERS["Authorization"]="Bearer {}".format(API_TOKEN)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/events_count/{off_set}")
def events_count(off_set: int):
    """Returns the total number of events grouped by the event type
    for a given offset"""
    return get_events_count(off_set,HEADERS,EVENT_TYPES)

@app.get("/avg_pull_request/{owner}/{repo_name}")
def avg_pull_request(owner: str,repo_name: str):
    """Returns average time between opened pull requests
    for a given repository"""
    return get_avg_time_between_repo_events(owner,repo_name,HEADERS,PULL_REQUEST_EVENT)