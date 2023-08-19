import requests
from datetime import datetime, timedelta

def get_events_count(off_set: int, headers: dict):
    url = "https://api.github.com/events"
    off_set_time = datetime.utcnow() - timedelta(minutes=off_set)
    response = requests.get(url=url, headers=headers)
    events = response.json()
    required_events = [event for event in events if event["type"] in ("WatchEvent","PullRequestEvent","IssuesEvent")]
    required_events_off_set = [event for event in required_events if datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ") > off_set_time]
    return required_events_off_set

if __name__ == "__main__":
    import os
    API_TOKEN = os.getenv("API_TOKEN", None)
    HEADERS = {
        "Accept":"application/vnd.github+json",
        "Authorization":"Bearer {}".format(API_TOKEN)
    }
    resp = get_events_count(10,HEADERS)
    print(resp)