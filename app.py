from flask import Flask, render_template, request, redirect
from google.cloud import vision
from google.cloud.vision import types
import simplejson as json
import base64

from google.oauth2 import service_account # temp

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

    elif language == "c" :

        source = '' + str(code)
        compiler = 11  # C

    elif language == "javascript":
        # source = 'function f() {return "hello"; } print(f());' # Javascript
        source = '' + str(code)
        compiler = 112  # Javascript

    else :
        #source = 'function f() {return "hello"; } print(f());' # Javascript
        source = '' + str(code)
        compiler = 112 # Javascript

    input = 'none'

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

        # Shortcircuit function:
        if client.submissions.get(response.get('id')).get('result').get('status').get('name') == 'runtime error' :
            print("ERROR: Runtime Error")
            return 'ERROR: Runtime Error'

        if client.submissions.get(response.get('id')).get('result').get('status').get('name') == 'compilation error' :
            print("ERROR: Compilation Error")
            return 'ERROR: Compilation Error'

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

@app.route("/intro")
def intro():
    return render_template("intro.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/runOCR", methods=['POST'])
def runOCR():
    GOOGLE_APPLICATION_CREDENTIALS = './key/CodeBoard-eb1f5c042ada.json' # temp
    credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)#temp

    content = json.loads(request.form['data'])['requests'][0]['image']['content']
    client = vision.ImageAnnotatorClient(credentials=credentials) # temp
    #client = vision.ImageAnnotatorClient()
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
        code = request.form['codetorun']
        lang = request.form['languages']
        types = request.form['types']

        # Parse input if function option selected
        if types == 'function' and lang == 'c':
            inputStr = request.form['functionInputs']

            # Parse Code
            # Grab function name
            codeParts = code.split()
            returnType = codeParts[0].strip() # get return type
            codeMoreParts = codeParts[1].split('(') # removes brackets

            rType = 'd'
            # if returnType == 'string' :
            #     rType = 's'

            code = '#include <stdio.h>\n#include <stdbool.h>\n#include <string.h>\n' + code + 'int main() { printf("%' + str(rType) + '",' + codeMoreParts[0] + '(' + inputStr + "));}"

        if types == 'function' and lang == 'javascript' :
            inputStr = request.form['functionInputs']

            # Parse Code
            # Grab function name
            codeParts = code.split()
            codeMoreParts = codeParts[1].split('(')

            code = code + 'print(' + codeMoreParts[0] + '(' + inputStr + '));'

        rawoutput = compileCode(code, lang)

    return render_template("results.html", rawoutput=rawoutput, incode=code)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    #app.run(debug=True, host='0.0.0.0')
    app.run(host='0.0.0.0')
