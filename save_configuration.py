import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('github')

def update_cursor(org:str, cur:str):

    response = table.update_item(
        Key={'key':"github"},
        ExpressionAttributeNames={
            "#v":"value",
            "#o":f"{org}"
        },
        ExpressionAttributeValues={
            ':v': f"{cur}"
        },
        UpdateExpression="SET #v.#o = :v",
    )

def lambda_handler(event, context):
    # TODO implement
    org = event['org']
    cur = event['cur']
    if cur is not None:
        update_cursor(event['org'], event['cur'])
    return {
        'statusCode': 200,
    }
