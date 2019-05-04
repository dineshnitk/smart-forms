import json
import os
import efficient_apriori
import boto3
import requests
import pickle
import time

AWS_ACCESS_KEY_ID='AKIAW745M2C2P5PSHHG2'
AWS_SECRET_ACCESS_KEY='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'
S3_BUCKET_NAME='smart-request-tracker'
BACKED_URL='http://52.24.109.247:8050'
BACKED_ENDPOINT='/smart/fields'
REQUEST_TYPES_ENDPOINT='/smart/requesttypes'
MIN_SUPPORT=0.5
MIN_CONFIDENCE=0.5

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
    url=BACKED_ENDPOINT + '/' + type
    content=requests.get(url)
    content_json = json.loads(content.text)
    transactions = [tuple((i.split(','))) for i in content_json["fields"]]

    # Build rules with given min_support and min_confidence
    itemsets, rules = efficient_apriori.apriori(transactions, min_support=MIN_SUPPORT,  min_confidence=MIN_CONFIDENCE)

    # Save rules in a local file
    filename=type + '.pkl'
    file = open('/tmp/' + filename, 'ab')
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
file = open('/tmp/' + filename, 'ab')
pickle.dump(rules, file)
file.close()

# Upload rule file to s3
client.upload_file('/tmp/' + filename, S3_BUCKET_NAME, filename)

# Return succss
return {
    'statusCode': 200,
    'body': json.dumps('Rules created/updated')
}
end = time.time()

# Print time taken for generating all the rules
print ("Time Taken (seconds):")
print (end - start)
