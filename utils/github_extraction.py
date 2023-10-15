import json
from utils import constant
import pip._vendor.requests as requests

url = constant.API_URL
headers = constant.GITHUB_HEADER

# {"announcement": null, "createdAt": "2012-01-18T01:30:18Z", "description": "Google ❤️ Open Source", "email": "opensource@google.com",, "name": "Google", "websiteUrl": "https://opensource.google/", "id": "MDEyOk9yZ2FuaXphdGlvbjEzNDIwMDQ=", "location": null, "url": "https://github.com/google"}

def extract_organization(organization_name:str):
    query = constant.ORGANIZATION_QUERY
    body = query.replace("__organization_name__", organization_name)
    try:
        response = requests.post(url, json={"query": body}, headers=headers)
        data = json.loads(response.content)
        return True, data['data']['organization']
    except Exception as e:
        print(e)
        return [False]
    
"""
['pageInfo']
    ['endCursor']
    ['hasNextPage']
['nodes']
    [
        ['id']
        ['createdAt']
        ['name']
        ['description']
        ['url']
    ]
"""

def extract_repository(organization_name:str, cursor = ""):
    query = constant.REPOSITORY_QUERY
    body = query.replace("__organization_name__", organization_name)
    body = body.replace("__cursor__", cursor)
    try:
        response = requests.post(url, json={"query": body}, headers=headers)
        data = json.loads(response.content)
        return True, data['data']['organization']['repositories']
    except Exception as e:
        print(e)
        return [False]

def extract_language(repository_id:str, cursor = ""):
    query = constant.LANGUAGE_QUERY
    body = query.replace("__repository_id__", repository_id)
    body = query.replace("__cursor__", cursor)
    response = requests.post(url, json={"query": body}, headers=headers)
    return json.loads(response.content)

def extract_pull_request(repository_id:str, cursor=""):
    query = constant.PULL_REQUEST_QUERY
    body = query.replace("__repository_id__", repository_id)
    body = body.replace("__cursor__", cursor)
    response = requests.post(url, json={"query": body}, headers=headers)
    return json.loads(response.content)

def extract_commit(repository_id:str, branch_cursor="", commit_cursor=""):
    query = constant.COMMIT_QUERY
    body = query.replace("__repository_id__", repository_id)
    body = body.replace("__branch_cursor__", branch_cursor)
    body = body.replace("__commit_cursor__", commit_cursor)
    response = requests.post(url, json={"query": body}, headers=headers)
    return json.loads(response.content)
