# Datamole Assignement
## Description
The aim of this assignment is to monitor activities happening on GitHub. For that we want you to stream specific events from the Github API (https://api.github.com/events). The events we are interested in are the WatchEvent, PullRequestEvent and IssuesEvent. Based on the collected events, metrics shall be provided at any time via a REST API to the end user. The following metrics should be implemented:  - Calculate the average time between pull requests for a given repository.  - Return the total number of events grouped by the event type for a given    offset. The offset determines how much time we want to look back i.e., an offset of 10 means we count only the events which have been created in the last 10 minutes. Bonus assignment  - Add another REST API endpoint providing a meaningful visualization of one of existing metrics or a newly introduced metric. Please add a README file to your solution that contains how to run the solution and a brief description about your assumptions. To get an idea of your documentation skills, we ask you to create a simple diagram of your application preferably regarding the C4 (level 1) model rules (https://c4model.com/). The assignment will have to be made in Python. We expect it will take 8 hours to do it properly.

## Events
Events interested in:
* WatchEvent
* PullRequestEvent
* IssuesEvent

## Metrics
Metrics to be implemented:
* Calculate the average time between pull requests for a given repository.
* Return the total number of events grouped by the event type for a given    offset. The offset determines how much time we want to look back i.e., an offset of 10 means we count only the events which have been created in the last 10 minutes. 
### Bonus
* Add another REST API endpoint providing a meaningful visualization of one of existing metrics or a newly introduced metric.

## Solution
To provide metrics to end users via a REST API I will need a API framework. Since this project is small I chose **FastAPI**. I haven't work with it yet, but I expect it to be lightweight and easy to use. Other options were Flask and Django. FastAPI will be used together with **uvicorn** as suggested by https://fastapi.tiangolo.com/#installation. For calling GitHub API I will use library **requests** and for manipulating with data library **numpy**.

All dependencies were saved to *requirements.txt* file.

### How to run it
Create virtual environment and activate it
```
$ python -m venv .venv
$ source .venv/Scripts/activate
```
install dependencies
```
$ pip install -r requirements.txt
```
run the ASGI web server
```
$ uvicorn main:app --reload
```
### Average time between pull requests
To get average time between pull requests go to website http://127.0.0.1:8000/avg_pull_request/{owner}/{repo_name} where *owner* and *repo_name* serve as placeholders for your values.

There are two actions related to PullRequestEvent *opened* and *closed*. In description of the assignement isn't described if I should include both, but since we want to know average time between pull requests it make sense to include only one of these actions. Otherwise the result could be misleading. For this reason I decided to only include *opened* actions. If it was intended to have both actions included, I would simple remove condition which is filtering *closed* events out.

Adding new parameter to the function with event type we are interested in would be a good idea for reusability of the code in the future.

### Total number of events
To get total number of events go to website http://127.0.0.1:8000/events_count/{off_set} where off_set serves as a placeholder for your value in minutes. Integer is expected.

Adding off set time key to response could be an option for a better overview from which timeframe we are receiving events.

### C4 Model (level 1)
![alt text](overview.jpg)