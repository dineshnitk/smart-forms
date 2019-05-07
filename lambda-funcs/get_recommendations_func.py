import json
import os
import efficient_apriori
import boto3
import requests
import pickle

AWS_ACCESS_KEY_ID=os.environ.get("aws_access_key_id")
AWS_SECRET_ACCESS_KEY=os.environ.get("aws_secret_access_key")
S3_BUCKET_NAME=os.environ.get("s3_bucket_name")
REQUEST_TYPES_ENDPOINT=os.environ.get("request_type_endpoint")

def get_recommendations_handler(event, context):
    input_type = event['queryStringParameters']['type']
    input_fields = event['queryStringParameters']['fields']

    input_list = input_fields.split(",")

    # Get list of all possible request types
    types=requests.get(REQUEST_TYPES_ENDPOINT)
    types_text=types.text.replace("[","").replace("]","").replace("\"","")
    types=list(types_text.split(","))

    rulefilename = 'rules.pkl'
    if input_type in types :
        rulefilename=input_type + '.pkl'

    client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    # Download association rules for the given type from s3
    client.download_file(S3_BUCKET_NAME, rulefilename, '/tmp/' + rulefilename)
    file = open('/tmp/' + rulefilename, 'rb')
    rules = pickle.load(file)
    file.close()

    # FIlter rules where given fields exist in the lhs
    rules_match = filter(lambda rule: all(x in list(rule.lhs) for x in input_list), rules)

    # From filtered rules, find the max length of rhs
    max_len_rhs=0
    for rule in rules_match:
        if(max_len_rhs < len(rule.rhs)):
            max_len_rhs = len(rule.rhs)
    print('max len of rhs amongst all matching rules = ' + str(max_len_rhs))

    result = ''
    if max_len_rhs > 0 :
    #    rules_rhs = filter(lambda rule: len(rule.rhs) == max_len_rhs , rules_match)
        rules_rhs = filter(lambda rule: all(x in list(rule.lhs) for x in input_list) and len(rule.rhs) == max_len_rhs, rules)
        sorted_rules = sorted(rules_rhs, key=lambda rule: rule.lift, reverse = True)
        result = ','.join(sorted_rules[0].rhs)

    message = {
        "result":result
    }
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body":json.dumps(message)
    }
