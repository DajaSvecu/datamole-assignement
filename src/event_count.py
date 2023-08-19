import requests
from datetime import datetime, timedelta

def get_events_count(off_set: int, headers: dict):
    url = "https://api.github.com/events"
    off_set_time = datetime.utcnow() - timedelta(minutes=off_set)
    counts = {
        "WatchEvent":0,
        "PullRequestEvent":0,
        "IssuesEvent":0,
        "OffSetTime":off_set_time.isoformat()
    }
    response = requests.get(url=url, headers=headers)
    while response:
        events = response.json()
        events_type = [event for event in events if event["type"] in ("WatchEvent","PullRequestEvent","IssuesEvent")]
        events_type_offset = [event["type"] for event in events_type if datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ") > off_set_time]
        for event in events_type_offset:
            counts[event] += 1
        if 'next' in response.links:
            next_url = response.links['next']['url']
            response = requests.get(next_url, headers=headers)
        else:
            # print("No more pages to retrieve.")
            break
    return counts

if __name__ == "__main__":
    import os,time
    API_TOKEN = os.getenv("API_TOKEN")
    if not API_TOKEN:
        raise EnvironmentError("Api Token not found!")

    HEADERS = {
        "Accept":"application/vnd.github+json",
        "Authorization":"Bearer {}".format(API_TOKEN)
    }
    start = time.time()
    resp = get_events_count(10,HEADERS)
    print(time.time()-start)
    print(resp)