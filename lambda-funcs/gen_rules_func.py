import json
import os
import efficient_apriori
import boto3
import requests
import pickle

AWS_ACCESS_KEY_ID=os.environ.get("aws_access_key_id")
AWS_SECRET_ACCESS_KEY=os.environ.get("aws_secret_access_key")
BACKED_ENDPOINT=os.environ.get("backend_endpoint")
REQUEST_TYPES_ENDPOINT=os.environ.get("request_types_endpoint")
S3_BUCKET_NAME=os.environ.get("s3_bucket_name")
MIN_SUPPORT=float(os.environ.get("min_support"))
MIN_CONFIDENCE=float(os.environ.get("min_confidence"))

def gen_rules_handler(event, context):
    # Get list of all possible request types
    types=requests.get(REQUEST_TYPES_ENDPOINT)
    # Convert them into list
    types_text=types.text.replace("[","").replace("]","").replace("\"","")
    types=list(types_text.split(","))

    client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    # Build Association rules for each type and save in S3
    for type in types :
        print("Generating association rules for type = " + type)

        # Get all records for the given type
        url=BACKED_ENDPOINT + '/' + type
        content=requests.get(url)
        content_json = json.loads(content.text)
        transactions = [tuple((i.split(','))) for i in content_json["fields"]]

        # Build rules with given min_support and min_confidence
        itemsets, rules = efficient_apriori.apriori(transactions, min_support=MIN_SUPPORT,  min_confidence=MIN_CONFIDENCE)

        # Save rules in a local file
        filename=type + '.pkl'
        file = open('/tmp/' + filename, 'wb')
        pickle.dump(rules, file)
        file.close()

        # Upload rule file to s3

        client.upload_file('/tmp/' + filename, S3_BUCKET_NAME, filename)

    # Genrate rules for all types
    print("Generating association rules for all types ")
    url=BACKED_ENDPOINT
    content=requests.get(url)
    content_json = json.loads(content.text)
    transactions = [tuple((i.split(','))) for i in content_json["fields"]]

    # Build rules with given min_support and min_confidence
    itemsets, rules = efficient_apriori.apriori(transactions, min_support=MIN_SUPPORT,  min_confidence=MIN_CONFIDENCE)

    # Save rules in a local file
    filename='rules.pkl'
    file = open('/tmp/' + filename, 'wb')
    pickle.dump(rules, file)
    file.close()

    # Upload rule file to s3
    client.upload_file('/tmp/' + filename, S3_BUCKET_NAME, filename)

    # Return succss
    return {
        'statusCode': 200,
        'body': json.dumps('Rules created/updated')
    }
