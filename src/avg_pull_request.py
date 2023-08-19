import requests
import numpy as np
from datetime import datetime

def get_avg_pull_request(owner: str, repo_name: str, headers: dict):
    """Calculates average time between opened pull requests for given repository"""
    url = "https://api.github.com/repos/{}/{}/events".format(owner,repo_name)
    timestamps = []
    response = requests.get(url=url,headers=headers)
    if response.status_code != 200:
        return {"ErrorMessage":"Repository was not found!"}

    while response:
        events = response.json()
        # Alternative would be to create for loop with two if statements if more readability
        new_timestamps = [event["created_at"] for event in events if event["type"] =="PullRequestEvent" and event["payload"]["action"]=="opened"]
        # Decided to get timestamps since epoch for better comparability
        timestamps_epoch = [datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").timestamp() for timestamp in new_timestamps]
        timestamps.extend(timestamps_epoch)
        if 'next' in response.links:
            next_url = response.links['next']['url']
            response = requests.get(next_url, headers=headers)
        else:
            # print("No more pages to retrieve.")
            break
    # Alternative - use library math, but numpy is cleaner option in my opinion
    timestamps_sort = sorted(timestamps)
    np_array = np.array(timestamps_sort)
    deltas = np.diff(np_array)
    mean = np.mean(deltas)
    return {
        "Owner": owner,
        "Repository": repo_name,
        "Average_pull_request":mean
    }

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