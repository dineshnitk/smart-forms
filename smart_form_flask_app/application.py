import os
import requests
import json

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)
#app.run(debug=True,port=5000)
endpoint_url = 'http://52.24.109.247:8050'

@app.route('/', methods=['GET', 'POST'])
def index(error=None):
    if request.method == 'POST':

        res = requests.get(endpoint_url + '/smart/requesttypes')
        types_text=res.text.replace("[","").replace("]","").replace("\"","")
        types=list(types_text.split(","))

        names = request.form.getlist('fieldname[]')
        vals = request.form.getlist("value[]")
        type = request.form.get("type")

        if type is None :
            error = "Must select a request type."
            return render_template('smartform.html', types=types,error=error)
        fields = []
        for (name,val) in zip(names,vals):
            field = {
                "name": name,
                "value": val
                }
            fields.append(field)
        smartform = {
            "fields": fields,
            "type": type
            }
        print(json.dumps(smartform))
        headers = {"Content-Type" : "application/json"}
        r = requests.post(endpoint_url + '/smart/request', data=json.dumps(smartform), headers=headers)
        if r.status_code != 200:
            print(r.text)
            error = "Error while saving this request. Please check your fields and try again."
            return render_template('smartform.html', types=types,error=error)
    req = requests.get(endpoint_url + '/smart/requests')
    forms = json.loads(req.text)
    # for form in forms :
    #     print( "type = " + str(form['type']))
    #     print( "id = " + str(form['id']))
    #     for field in form['fields']:
    #         print('\tname = ' + field['name'])
    #         print('\tvalue = ' + field['value'])
    #     print('######')
    return render_template('index.html',forms=forms)

@app.route('/smartform', methods=['GET', 'POST'])
def smartform():
    res = requests.get(endpoint_url + '/smart/requesttypes')
    types_text=res.text.replace("[","").replace("]","").replace("\"","")
    types=list(types_text.split(","))
    print(types)
    return render_template('smartform.html', types=types,error=None)

@app.route('/deleteform/<id>', methods=['GET', 'POST'])
def deleteform(id):
    requests.delete(endpoint_url + '/smart/request/' + str(id))
    return redirect(url_for('index'))
