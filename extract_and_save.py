from utils import github_extraction, constant, s3_function, dynamodb_function
import os

def datetime_to_path(input_time:str):
    date, time = input_time.split(' ')
    year, month, day = date.split('-')
    hour, minute, second = time.split(':')
    return f'/year={year}/month={month}/day={day}/hour={hour}/minute={minute}/'

# Chưa save id parent 

"""
['in']
    ['extract']
        ['object']
        ['config']
            ['type']
            ['parent']
            ['interval']
            ['key']
        ['time_window']
            ['from']
            ['to']
        ['children']
    ['ancient']
        ['organization']
        ['organization_id']
    ['parent']
    ['extra']

['out']
    ['extract']
    ['ancient']
        ['organization']
        ['organization_id']
        ['repository_cursor']
    ['children']
    ['extra']
"""

def extract(event:dict):
    result = {}
    parent_info = event['parent']
    result['ancient'] = event['ancient'] if 'ancient' in event else {}
    extract_info = result['extract'] = event['extract']
    result['extra'] = event['extra'] if 'extra' in event else {}
    result['extra']['has_err'] = False
    result['extra']['count'] = result['extra']['count'] + 1 if 'count' in result['extra'] else 1
    result['extra']['count'] = 1 if result['extra']['count'] > 5 else result['extra']['count']
    
    
    file_path = f'{constant.S3_FOLDER}/object={extract_info["object"]}' + datetime_to_path(extract_info['time_window']['to'])
    
    if extract_info['object'] == "organization":
        has_data, data = github_extraction.extract_organization(parent_info['organization'])

        if has_data == True:
            result['ancient']['organization'] = data['name']
            result['ancient']['organization_id'] = data['id']
            result['ancient']['repository_cursor'] = parent_info['repository_cursor']

            if parent_info['repository_cursor'] == '':
                file_organization_path = file_path + f'{parent_info["organization_id"]}'
                try:
                    s3_function.save_parquet_to_s3(file_organization_path, data)
                except Exception as e:
                    print(e)
                    print("has a error when save to s3")
                    result['extra']['has_err'] = True
        else:
            result['extra']['has_err'] = True
            print("out of organization data")

    elif extract_info['object'] == "repository":
        has_data, data = github_extraction.extract_repository(result['ancient']['organization'], result['ancient']['repository_cursor'])

        if has_data == True:
            file_repository_path = file_path + f'{data["pageInfo"]["endCursor"]}'

            parent_ids ={}
            parent_ids['organization_id'] = result['ancient']['organization_id']
            result['ancient']['repository_cursor'] = data["pageInfo"]["endCursor"]
            result['extra']['has_next'] = data["pageInfo"]["hasNextPage"]
            result['children'] = data['nodes']

            try:
                s3_function.save_parquet_to_s3(file_repository_path, data['nodes'], parent_ids)
                dynamodb_function.update_cursor(result['ancient']['organization'], data["pageInfo"]["endCursor"])
            except Exception as e:
                print(e)
                print("has a error when save to s3")
                result['extra']['has_err'] = True
        else:
            result['extra']['has_err'] = True
            print(f"out of repository in {parent_info['organization']} organization data")
        
    elif extract_info['object'] == "pullRequest":
        result['ancient']['repository_id'] = event['parent']['id']
        result['ancient']['repository'] = event['parent']['name']
        result['ancient']['pull_request_cusor'] = result['ancient']['pull_request_cusor'] if 'pull_request_cusor' in result['ancient'] else ""

        has_data, data = github_extraction.extract_pull_request(event['parent']['id'], result['ancient']['pull_request_cusor'])

        if has_data == True:
            file_repository_path = file_path + f'{data["pageInfo"]["endCursor"]}'

            parent_ids ={}
            parent_ids['repository_id'] = event['parent']['id']

            result['ancient']['pull_request_cusor'] = data["pageInfo"]["endCursor"]
            result['extra']['has_next'] = data["pageInfo"]["hasNextPage"]
            result['children'] = data['nodes']

            try:
                s3_function.save_parquet_to_s3(file_repository_path, data['nodes'], parent_ids)
            except Exception as e:
                print(e)
                print("has a error when save to s3")
                result['extra']['has_err'] = True
        else:
            result['extra']['has_err'] = True
            print(f"out of pull requests in {parent_info['repository']} repository data")

    elif extract_info['object'] == "language":
        result['ancient']['repository_id'] = event['parent']['id']
        result['ancient']['repository'] = event['parent']['name']
        result['ancient']['language_cusor'] = result['ancient']['language_cusor'] if 'language_cusor' in result['ancient'] else ""

        has_data, data = github_extraction.extract_pull_request(event['parent']['id'], result['ancient']['language_cusor'])

        if has_data == True:
            file_repository_path = file_path + f'{data["pageInfo"]["endCursor"]}'

            parent_ids ={}
            parent_ids['repository_id'] = event['parent']['id']

            result['ancient']['language_cusor'] = data["pageInfo"]["endCursor"]
            result['extra']['has_next'] = data["pageInfo"]["hasNextPage"]
            result['children'] = data['nodes']

            try:
                s3_function.save_parquet_to_s3(file_repository_path, data['nodes'], parent_ids)
            except Exception as e:
                print(e)
                print("has a error when save to s3")
                result['extra']['has_err'] = True
        else:
            result['extra']['has_err'] = True
            print(f"out of language in {parent_info['repository']} repository data")

    elif extract_info['object'] == "branch":
        result['ancient']['repository_id'] = event['parent']['id']
        result['ancient']['repository'] = event['parent']['name']
        result['ancient']['branch_cursor'] = result['ancient']['branch_cursor'] if 'branch_cursor' in result['ancient'] else ""

        has_data, data = github_extraction.extract_branch(event['parent']['id'], result['ancient']['branch_cursor'])

        if has_data == True:
            file_repository_path = file_path + f'{data["pageInfo"]["endCursor"]}'

            parent_ids ={}
            parent_ids['repository_id'] = event['parent']['id']

            result['ancient']['branch_cursor'] = data["pageInfo"]["endCursor"]
            result['extra']['has_next'] = data["pageInfo"]["hasNextPage"]
            result['children'] = data['nodes']

            try:
                s3_function.save_parquet_to_s3(file_repository_path, data['nodes'], parent_ids)
            except Exception as e:
                print(e)
                print("has a error when save to s3")
                result['extra']['has_err'] = True

        else:
            result['extra']['has_err'] = True
            print(f"out of branch in {parent_info['repository']} repository data")

    elif extract_info['object'] == "commit":
        result['ancient']['branch_id'] = event['parent']['id']
        result['ancient']['branch'] = event['parent']['name']
        result['ancient']['branch_cursor'] = result['ancient']['branch_cursor'] if 'branch_cursor' in result['ancient'] else ""
        result['ancient']['commit_cursor'] = result['ancient']['commit_cursor'] if 'commit_cursor' in result['ancient'] else ""

        has_data, data = github_extraction.extract_commit(result['ancient']['repository_id'], result['ancient']['branch_cursor'], result['ancient']['commit_cursor'])

        if has_data == True:
            file_repository_path = file_path + f'{data["pageInfo"]["endCursor"]}'

            parent_ids ={}
            parent_ids['branch_id'] = event['parent']['id']

            result['ancient']['commit_cursor'] = data["pageInfo"]["endCursor"]
            result['extra']['has_next'] = data["pageInfo"]["hasNextPage"]
            result['children'] = data['nodes']

            try:
                s3_function.save_parquet_to_s3(file_repository_path, data['nodes'], parent_ids)
            except Exception as e:
                print(e)
                print("has a error when save to s3")
                result['extra']['has_err'] = True
        else:
            result['extra']['has_err'] = True
            print(f"out of branch in {parent_info['repository']} repository data")

if __name__ == "__main__":
    # has_data, data = github_extraction.extract_repository("google")
    print(github_extraction.extract_pull_request("MDEwOlJlcG9zaXRvcnkxOTM2Nzcx"))
    pass
    
    
