import requests
import numpy as np
from datetime import datetime
import timeit

def get_avg_pull_request(owner: str, repo_name: str, headers: dict):
    url = "https://api.github.com/repos/{}/{}/events".format(owner,repo_name)
    timestamps = []
    response = requests.get(url=url,headers=headers)

    while response:
        events = response.json()
        new_timestamps = [event["created_at"] for event in events if event["type"] =="PullRequestEvent" and event["payload"]["action"]=="opened"]
        # 
        timestamps_epoch = [datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").timestamp() for timestamp in new_timestamps]
        timestamps.extend(timestamps_epoch)
        if 'next' in response.links:
            next_url = response.links['next']['url']
            response = requests.get(next_url, headers=headers)
        else:
            # print("No more pages to retrieve.")
            break
    timestamps_sort = sorted(timestamps)
    np_array = np.array(timestamps_sort)
    deltas = np.diff(np_array)
    mean = np.mean(deltas)
    return mean
    
if __name__ == "__main__":
    import os,time,json
    API_TOKEN = os.getenv("API_TOKEN")
    if not API_TOKEN:
        raise EnvironmentError("Api Token not found!")

    HEADERS = {
        "Accept":"application/vnd.github+json",
        "Authorization":"Bearer {}".format(API_TOKEN)
    }
    OWNER = "mertpekey"
    REPO_NAME = "DeepKinZero"
    result = timeit.timeit(lambda : get_avg_pull_request(OWNER,REPO_NAME,HEADERS),number=30)
    print(result)
    # resp.sort(key= lambda x: x["created_at"])
    # for res in resp: