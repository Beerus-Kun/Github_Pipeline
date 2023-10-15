

def lambda_handler(event, context):
    org_info = fetch_cursor()
    return {
        'org_info' : org_info
    }