import json
from utils import constant
import requests

url = constant.API_URL
headers = constant.GITHUB_HEADER

def handle_cursor(cursor:str):
    return "" if cursor.strip() == "" else "after: " + '"' + cursor + '"'
    
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

def extract_repository(organization_name:str, cursor = ""):
    query = constant.REPOSITORY_QUERY
    cursor = handle_cursor(cursor)
    body = query.replace("__organization_name__", organization_name)
    body = body.replace("__cursor__", cursor)
    try:
        response = requests.post(url, json={"query": body}, headers=headers)
        data = json.loads(response.content)
        return True, data['data']['organization']['repositories']
    except Exception as e:
        print(e)
        return [False]

def extract_pull_request(repository_id:str, cursor=""):
    query = constant.PULL_REQUEST_QUERY
    cursor = handle_cursor(cursor)
    body = query.replace("__repository_id__", repository_id)
    body = body.replace("__cursor__", cursor)
    try:
        response = requests.post(url, json={"query": body}, headers=headers)
        data = json.loads(response.content)
        return True, data['data']['node']['pullRequests']
    except Exception as e:
        print(e)
        return [False]
    
def extract_language(repository_id:str, cursor = ""):
    query = constant.LANGUAGE_QUERY
    cursor = handle_cursor(cursor)
    body = query.replace("__repository_id__", repository_id)
    body = query.replace("__cursor__", cursor)
    try:
        response = requests.post(url, json={"query": body}, headers=headers)
        data = json.loads(response.content)
        return True, data['data']['node']['languages']
    except Exception as e:
        print(e)
        return [False]

def extract_branch(repository_id:str, branch_cursor = ""):
    query = constant.BRANCH_QUERY
    branch_cursor = handle_cursor(branch_cursor)
    body = query.replace("__repository_id__", repository_id)
    body = query.replace("__branch_cursor__", branch_cursor)
    try:
        response = requests.post(url, json={"query": body}, headers=headers)
        data = json.loads(response.content)
        return True, data['data']['node']['refs']
    except Exception as e:
        print(e)
        return [False]

def extract_commit(repository_id:str, branch_cursor="", commit_cursor=""):
    query = constant.COMMIT_QUERY
    branch_cursor = handle_cursor(branch_cursor)
    commit_cursor = handle_cursor(commit_cursor)
    body = query.replace("__repository_id__", repository_id)
    body = body.replace("__branch_cursor__", branch_cursor)
    body = body.replace("__commit_cursor__", commit_cursor)
    try:
        response = requests.post(url, json={"query": body}, headers=headers)
        data = json.loads(response.content)
        return True, data['data']['node']['refs']['nodes'][-1]['target']['history']
    except Exception as e:
        print(e)
        return [False]
