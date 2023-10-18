import boto3, json, io
import pandas as pd
from utils import constant

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

def save_json(id:str, content:dict):
    s3_client.put_object(Key=id, Bucket=constant.BUCKET, Body=json.dumps(content))

def read_json(file_key):
    response = s3_client.get_object(Bucket=constant.BUCKET, Key=file_key)
    file_content = response['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    return json_content

def read_txt(file_key):
    print(read_txt)
    print(file_key)
    s3_object = s3_client.get_object(Bucket=constant.BUCKET, Key=file_key)
    body = s3_object['Body']
    return body.read().decode('utf-8')

def move_file(from_key, to_key):
    print('move file')
    print(from_key)
    print(to_key)
    copy_source = {
        'Bucket': constant.BUCKET,
        'Key': from_key
    }
    s3_resource.meta.client.copy(copy_source, constant.BUCKET, to_key)

def delete_file(folder_link):
    bucket = s3_resource.Bucket(constant.BUCKET)
    bucket.object_versions.filter(Prefix=folder_link).delete()

def save_parquet_to_s3(file_path:str, data:dict, parents:dict = {}):
    file_path = file_path + constant.PARQUET_EXTENSION
    df = pd.DataFrame.from_dict(data)

    for key, value in parents.items():
        df[key] = value

    out_buffer = io.BytesIO()
    df.to_parquet(out_buffer, index=False)

    s3_client.put_object(Bucket=constant.BUCKET, Key=file_path, Body=out_buffer.getvalue())