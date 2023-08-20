import requests
from datetime import datetime, timedelta

def get_events_count(off_set: int, headers: dict, event_types:tuple):
    """Returns total number of events grouped by the event type"""
    url = "https://api.github.com/events"
    off_set_time = datetime.utcnow() - timedelta(minutes=off_set)
    events = []
    response = requests.get(url=url, headers=headers, params={"per_page":100})
    while response:
        events.extend(response.json())
        if 'next' not in response.links:
            break
        next_url = response.links['next']['url']
        response = requests.get(next_url, headers=headers)
    return process_events(events, off_set_time,event_types)

def process_events(events:list, off_set_time: datetime, event_types: tuple) -> dict:
    """Processes events and return total count per event type"""
    counts = {event_type:0 for event_type in event_types}
    for event in events:
        if event["type"] not in event_types:
            continue
        if datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ") > off_set_time:
            counts[event["type"]] +=1
    return counts

# Testing purposes
if __name__ == "__main__":
    import os,timeit
    EVENT_TYPES = ("WatchEvent","PullRequestEvent","IssuesEvent")
    HEADERS = {
        "Accept":"application/vnd.github+json",
    }
    # API_TOKEN = os.getenv("API_TOKEN")
    # if API_TOKEN:
    #     HEADERS["Authorization"]="Bearer {}".format(API_TOKEN)

    result = timeit.timeit(lambda: get_events_count(10, HEADERS, EVENT_TYPES),number=30)
    print(result)