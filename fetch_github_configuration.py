import boto3

# conect to dynamodb
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('github')

def fetch_cursor():
    response = table.get_item(
        Key={
            'key':"github"
        }
    )

    res = []
    for org, cur in response['Item']['value'].items():
        res.append({"org": org, "cur":cur})
    return res

def lambda_handler(event, context):
    org_info = fetch_cursor()
    return {
        'org_info' : org_info
    }