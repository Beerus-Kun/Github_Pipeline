import boto3, json, requests

s3_client = boto3.client('s3')

def save_to_s3(id:str, content:dict):
    
    s3_client.put_object(Key=f"simple-github/{id}.json", Bucket="github-datalake", Body=json.dumps(content))


def fetch_data(org, cur):
    url = "https://api.github.com/graphql"

    organization_line = f'organization(login: "{org}")'
    repository_line = f'repositories(first: 100 after:"{cur}")'

    body = "query {" + organization_line + "{" + repository_line + """ {
            pageInfo{
                endCursor
                hasNextPage
            }
            nodes {
                id
                name
                url
            }
            }
        }
    }
    """
    headers = {"Authorization": f"Bearer "}
    response = requests.post(url, json={"query": body}, headers=headers)
    return json.loads(response.content)
    

def lambda_handler(event, context):
    # TODO implement
    data = fetch_data(event['org'], event['cur'])
    for repository in data['data']['organization']['repositories']['nodes']:
        save_to_s3(repository['id'], repository)
    
    
    return {
        'hasNextPage': data['data']['organization']['repositories']['pageInfo']['hasNextPage'],
        'cur': data['data']['organization']['repositories']['pageInfo']['endCursor'],
        'org': event['org']
    }
