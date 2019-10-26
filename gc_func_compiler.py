from sphere_engine import CompilersClientV4
from sphere_engine.exceptions import SphereEngineException

import time

#respond to an http request
def hello_world(request):

    # define access parameters
    accessToken = '77501c36922866a03b1822b4508a50c6'
    endpoint = 'dd57039c.compilers.sphere-engine.com'

    # initialization
    client = CompilersClientV4(accessToken, endpoint)

    # API usage
    # source = 'function f() {return "hello"; } print(f());' # Javascript
    # compiler = 112 # Javascript

    # source = 'print("hello world please work!!!!!")' # Python
    
    # extract text from json and assign to source
    request_json = request.get_json()
    cource = request.args.get('message')
    
    
    compiler = 116 # Python

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
    while client.submissions.get(response.get('id')).get('result').get('status').get('name') != 'accepted' :
        responseData = client.submissions.get(response.get('id'))
        print(responseData) # for test purposes
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
            print('Non existing resource, error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))
        elif e.code == 400:
            print('Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))

    #print("Output returned is: ")
    #print(rawresponse)

    return(rawresponse)
    #return response to requester
    