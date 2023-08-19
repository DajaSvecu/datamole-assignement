import requests
from datetime import datetime, timedelta

def get_events_count(off_set: int, headers: dict):
    """Returns total number of events grouped by the event type"""
    url = "https://api.github.com/events"
    off_set_time = datetime.utcnow() - timedelta(minutes=off_set)
    counts = {
        "WatchEvent":0,
        "PullRequestEvent":0,
        "IssuesEvent":0,
    }
    response = requests.get(url=url, headers=headers)
    while response:
        events = response.json()
        for event in events:
            # For better readability the conditions were separated
            # other would be put in to one if statement
            if event["type"] not in ("WatchEvent","PullRequestEvent","IssuesEvent"):
                continue
            if datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ") > off_set_time:
                counts[event["type"]] +=1
        if 'next' in response.links:
            next_url = response.links['next']['url']
            response = requests.get(next_url, headers=headers)
        else:
            # print("No more pages to retrieve.")
            break
    return counts

# Testing purposes
if __name__ == "__main__":
    import os,timeit
    HEADERS = {
        "Accept":"application/vnd.github+json",
    }
    API_TOKEN = os.getenv("API_TOKEN")
    if API_TOKEN:
        HEADERS["Authorization"]="Bearer {}".format(API_TOKEN)

    result = timeit.timeit(lambda: get_events_count(10, HEADERS),number=30)
    print(result)