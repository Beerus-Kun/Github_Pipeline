from utils import github_extraction, constant, s3_function, dynamodb_function
import os



def datetime_to_path(input_time:str):
    date, time = input_time.split(' ')
    year, month, day = date.split('-')
    hour, minute, second = time.split(':')
    return f'/year={year}/month={month}/day={day}/hour={hour}/minute={minute}/'

"""
    configs['parent_info']
        ['organization']
        ['organization_id']
        ['repository_cursor']
    configs['extract_info']
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
"""

def extract(configs:dict):
    parent_info = configs['parent_info']
    extract_info = configs['extract_info']
    has_err = False

    file_path = f'object={extract_info["object"]}' + datetime_to_path(extract_info['time_window']['to'])
    
    if extract_info['object'] == "organization":
        if parent_info['repository_cursor'] == '':
            has_data, data = github_extraction.extract_organization(parent_info['organization'])

            if has_data == True:
                parent_info['organization'] = data['name']
                parent_info['organization_id'] = data['id']

                file_organization_path = file_path + f'{parent_info["organization_id"]}{constant.PARQUET_EXTENSION}'
                s3_function.save_parquet_to_s3(file_organization_path, data)
            else:
                has_err = True
                print("out of organization data")

        has_data, data = github_extraction.extract_repository(parent_info['organization'], parent_info['repository_cursor'])

        if has_data == True:
            file_repository_path = file_path + f'{extract_info["pageInfo"]["endCursor"]}{constant.PARQUET_EXTENSION}'
            s3_function.save_parquet_to_s3(file_repository_path, data)
            dynamodb_function.update_cursor(parent_info['organization'], extract_info["pageInfo"]["endCursor"])
        else:
            print(f"out of repository in {parent_info['organization']} organization data")
        
    elif extract_info['object'] == "repository":
        has_data, data = github_extraction.extract_repository(parent_info['organization'], parent_info['repository_cursor'])

        if has_data == True:
            parent_info['repository'] = data['name']
            parent_info['repository_id'] = data['id']
            save_parquet_to_s3(file_path, data)
        else:
            print("none")

if __name__ == "__main__":
    # has_data, data = github_extraction.extract_repository("google")
    print(github_extraction.extract_repository("google"))
    pass
    
    
