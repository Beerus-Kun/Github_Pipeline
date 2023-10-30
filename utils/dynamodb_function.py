import boto3
from utils import constant

# conect to dynamodb
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(constant.DYNAMODB_TABLE)

def get_organization_cursor():
    response = table.get_item(
        Key={
            'key': constant.DYNAMODB_ITEM
        }
    )

    res = []
    for org, cur in response['Item']['value'].items():
        res.append({"organization": org, "repository_cursor":cur})
    return res

def update_cursor(org:str, cur:str):

    table.update_item(
        Key={'key':constant.DYNAMODB_ITEM},
        ExpressionAttributeNames={
            "#v":"value",
            "#o":f"{org}"
        },
        ExpressionAttributeValues={
            ':v': f"{cur}"
        },
        UpdateExpression="SET #v.#o = :v",
    )

if __name__ == "__main__":
    print(get_organization_cursor())