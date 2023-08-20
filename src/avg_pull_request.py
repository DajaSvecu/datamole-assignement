import requests
import numpy as np
from datetime import datetime,timedelta

def get_avg_time_between_repo_events(owner: str, repo_name: str, headers: dict, event_type: str) -> dict:
    """Returns average time between opened pull requests for given repository"""
    url = "https://api.github.com/repos/{}/{}/events".format(owner,repo_name)
    events = []
    response = requests.get(url=url,headers=headers,params={"per_page":100})
    if response.status_code != 200:
        return {"ErrorMessage":"Error occured!","StatusCode": response.status_code}

    while response:
        events.extend(response.json())
        if 'next' not in response.links:
            break
        next_url = response.links['next']['url']
        response = requests.get(next_url, headers=headers)

    mean = calculate_mean_between_events(events, event_type)
    # mean = calculate_mean_between_events_action(events, event_type, "opened")
    return {
        "Owner": owner,
        "Repository": repo_name,
        "AveragePullRequest": timedelta(seconds=mean).__str__(),
        "AveragePullRequestSeconds":mean,
    }

def calculate_mean_between_events(events:list, event_type:str) -> float:
    """Calculates average time between events for given
    event type and returns it in seconds """
    timestamps = []
    for event in events:
        if event["type"] != event_type:
            continue
        timestamps.append(datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ").timestamp())
    timestamps_sorted = sorted(timestamps)
    np_array = np.array(timestamps_sorted)
    deltas = np.diff(np_array)
    return np.mean(deltas)

def calculate_mean_between_events_action(events:list, event_type:str, action:str) -> float:
    """Calculates average time between events for given
    event type and action and returns it in seconds """
    timestamps = []
    for event in events:
        if event["type"] != event_type or event["payload"]["action"] != action:
            continue
        timestamps.append(datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ").timestamp())
    timestamps_sorted = sorted(timestamps)
    np_array = np.array(timestamps_sorted)
    deltas = np.diff(np_array)
    return np.mean(deltas)

# Testing purposes
if __name__ == "__main__":
    import os, timeit
    HEADERS = {
        "Accept":"application/vnd.github+json",
    }
    API_TOKEN = os.getenv("API_TOKEN")
    if API_TOKEN:
        HEADERS["Authorization"]="Bearer {}".format(API_TOKEN)

    OWNER = "mertpekey"
    REPO_NAME = "DeepKinZero"
    result = timeit.timeit(lambda : get_avg_pull_request(OWNER,REPO_NAME,HEADERS),number=30)
    print(result)