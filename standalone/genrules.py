import json
import os
import efficient_apriori
import boto3
import requests
import pickle
import time
import configparser

configParser = configparser.RawConfigParser()
configFilePath = r'./config.props'
configParser.read(configFilePath)

AWS_ACCESS_KEY_ID = configParser.get('PARAMS', 'AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = configParser.get('PARAMS', 'AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = configParser.get('PARAMS', 'S3_BUCKET_NAME')
SMART_FIELDS_ENDPOINT = configParser.get('PARAMS', 'BACKEND_URL') + configParser.get('PARAMS', 'SMART_FIELDS_ENDPOINT')
REQUEST_TYPES_ENDPOINT = configParser.get('PARAMS', 'BACKEND_URL') + configParser.get('PARAMS', 'REQUEST_TYPES_ENDPOINT')
MIN_SUPPORT = float(configParser.get('PARAMS', 'MIN_SUPPORT'))
MIN_CONFIDENCE = float(configParser.get('PARAMS', 'MIN_CONFIDENCE'))

# Capture start time
start = time.time()

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
    url=SMART_FIELDS_ENDPOINT + '/' + type
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

    print("List of rules for type = " + type)
    for rule in rules :
        print(rule)

    # # Upload rule file to s3
    client.upload_file('/tmp/' + filename, S3_BUCKET_NAME, filename)

# Genrate rules for all types
print("Generating association rules for all types ")
url=SMART_FIELDS_ENDPOINT
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

print("Rules created successfully")

end = time.time()

# Print time taken for generating all the rules
print ("Time Taken (seconds):")
print (end - start)
