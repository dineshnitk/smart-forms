import os
import requests
import efficient_apriori
import pickle
import boto3
import awscli
from flask import Flask, request, jsonify
app = Flask(__name__)

AWS_ACCESS_KEY_ID=''
AWS_SECRET_ACCESS_KEY=''
S3_BUCKET_NAME=''

@app.route("/api/recommendation")
def recommendation_api():
        input_type=request.args.get('type')
        input_fields=request.args.get('fields')
        print(input_type)
        print(input_fields)

        print('Recommendations for type = ' + input_type)
        rulefilename=input_type + '.pkl'
        input_list = input_fields.split(",")
        client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        client.download_file(S3_BUCKET_NAME, rulefilename, '/tmp/' + rulefilename)
        file = open('/tmp/' + rulefilename, 'rb')
        rules = pickle.load(file)
        file.close()

        max_len_rhs=0
        for rule in rules:
            if(max_len_rhs < len(rule.rhs)):
                max_len_rhs = len(rule.rhs)

        print('max len on rhs = ' + str(max_len_rhs))

        i=max_len_rhs
        while i > 0 :
            rules_rhs = filter(lambda rule: all(x in list(rule.lhs) for x in input_list) and len(rule.rhs) == i , rules)
            sorted_rules = sorted(rules_rhs, key=lambda rule: rule.lift, reverse = True)
            if len(sorted_rules) != 0 :
                result = ','.join(sorted_rules[0].rhs)
                print(result)
                return jsonify({
                    "result":result
                })
            i = i-1
        return jsonify({
            "result":""
        })
