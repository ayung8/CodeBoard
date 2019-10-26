from flask import Flask, render_template, request, redirect
from google.cloud import vision
from google.cloud.vision import types
import simplejson as json
import base64

from sphere_engine import CompilersClientV4
from sphere_engine.exceptions import SphereEngineException

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

import time

app = Flask(__name__)

def compileCode(code, language = "javascript") :
    # define access parameters
    accessToken = '77501c36922866a03b1822b4508a50c6'
    endpoint = 'dd57039c.compilers.sphere-engine.com'

    # initialization
    client = CompilersClientV4(accessToken, endpoint)

    # API usage

    if language == "python" :
        #source = 'print("hello world please work!!!!!")'  # Python
        source = '' + str(code)
        compiler = 116  # Python

    elif language == "javascript" :
        # source = 'function f() {return "hello"; } print(f());' # Javascript
        source = '' + str(code)
        compiler = 112  # Javascript

    else :
        #source = 'function f() {return "hello"; } print(f());' # Javascript
        source = '' + str(code)
        compiler = 112 # Javascript

    input = '2017'

    # Set default value for response
    response = None

    # Sends the submission and checks for errors in sending the submission
    try:
        response = client.submissions.create(source, compiler, input)
        # response['id'] stores the ID of the created submission
    except SphereEngineException as e:
        if e.code == 401:
            print('Invalid access token')
        elif e.code == 402:
            print('Unable to create submission')
        elif e.code == 400:
            print('Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))

    # Set default value for response data
    responseData = None

    print("Code submitted is: ")
    print(source)
    print("Submission ID is: " + str(response.get('id')))
    print()

    # Try getting submission ID and check if there are errors
    try:
        client.submissions.get(response.get('id'))
    except SphereEngineException as e:
        if e.code == 401:
            print('Invalid access token')
        elif e.code == 403:
            print('Access to the submission is forbidden')
        elif e.code == 404:
            print('Submission does not exist')

    # Uses submission ID, and checks every x seconds to see if query has been 'accepted' (finished processing)
    while client.submissions.get(response.get('id')).get('result').get('status').get('name') != 'accepted':
        responseData = client.submissions.get(response.get('id'))
        print(responseData)  # for test purposes
        print("Status is: " + responseData.get('result').get('status').get('name'))
        time.sleep(5)

    print("Status is: " + client.submissions.get(response.get('id')).get('result').get('status').get('name'))
    print()

    rawresponse = None

    # Get the output of the query
    try:
        rawresponse = client.submissions.getStream(response.get('id'), 'output')
    except SphereEngineException as e:
        if e.code == 401:
            print('Invalid access token')
        elif e.code == 403:
            print('Access to the submission is forbidden')
        elif e.code == 404:
            print('Non existing resource, error code: ' + str(
                e.error_code) + ', details available in the message: ' + str(e))
        elif e.code == 400:
            print('Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))

    print("Output returned is: ")
    print(rawresponse)

    return rawresponse

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/runOCR", methods=['POST'])
def runOCR():
    content = json.loads(request.form['data'])['requests'][0]['image']['content']
    client = vision.ImageAnnotatorClient()
    image = types.Image(content = base64.b64decode(content))
    response = client.document_text_detection(image=image)
    if (len(response.text_annotations) < 1):
        return "no text found"
    else:
        #print(response.text_annotations[0].description)
        return response.text_annotations[0].description

@app.route("/output", methods=['GET', 'POST'])
def getOutput():
    rawoutput = "NONE"

    if request.method == 'POST':
        code = request.form['code']
        # lang = request.form['language']

        # Call function to get raw output
        rawoutput = compileCode(code)
        # rawoutput = compileCode(code, lang)

    return render_template("file.html", rawoutput=rawoutput)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    #app.run(debug=True, host='0.0.0.0')
    app.run(host='0.0.0.0')
