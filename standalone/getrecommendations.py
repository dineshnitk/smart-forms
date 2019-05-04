import json
import os
import efficient_apriori
import boto3
import requests
import pickle
import time

start = time.time()

AWS_ACCESS_KEY_ID='AKIAW745M2C2P5PSHHG2'
AWS_SECRET_ACCESS_KEY='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'
S3_BUCKET_NAME='smart-request-tracker'

# http://54.213.20.229:5000/api/recommendation?type=CLINICTRIAL&fields=type
# input_type=request.args.get('type')
# input_fields=request.args.get('fields')
# Use sample values for input type and fields
input_type="CLINICTRIAL"
input_fields="type"

print('Getting recommendations for type = ' + input_type + " and fields = " + input_fields)

rulefilename=input_type + '.pkl'
input_list = input_fields.split(",")
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

if max_len_rhs > 0 :
#    rules_rhs = filter(lambda rule: len(rule.rhs) == max_len_rhs , rules_match)
    rules_rhs = filter(lambda rule: all(x in list(rule.lhs) for x in input_list) and len(rule.rhs) == max_len_rhs, rules)
    sorted_rules = sorted(rules_rhs, key=lambda rule: rule.lift, reverse = True)
    result = ','.join(sorted_rules[0].rhs)
    print(result)
    # return jsonify({
    #     "result":result
    # })
#  return jsonify({
#     "result":""
# })

end = time.time()
print ("Time Taken (seconds):")
print (end - start)
