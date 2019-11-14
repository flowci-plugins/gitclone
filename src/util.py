import os
import json
import sys
import base64
import http.client

ServerUrl = os.environ.get('FLOWCI_SERVER_URL')
FlowName = os.environ.get("FLOWCI_FLOW_NAME")
BuildNumber = os.environ.get("FLOWCI_JOB_BUILD_NUM")
AgentToken = os.environ.get('FLOWCI_AGENT_TOKEN')
AgentJobDir = os.environ.get('FLOWCI_AGENT_JOB_DIR')

HttpHeaders = {
    "Content-type": "application/json",
    "AGENT-TOKEN": AgentToken
}

def createDir(path):
    try:
        return os.makedirs(path)
    except FileExistsError:
        return path

def getVar(name, required = True):
    val = os.environ.get(name)
    if required and val is None:
        sys.exit("{} is missing".format(name))
    return val

def createHttpConn(url):
    if url.startswith("http://"):
        return http.client.HTTPConnection(url.lstrip("http://"))

    return http.client.HTTPConnection(url.lstrip("https://"))

def fetchCredential(name):
    try:
        path = "/api/credential/{}".format(name)
        conn = createHttpConn(ServerUrl)
        conn.request(method = "GET", url = path, headers = HttpHeaders)
         
        response = conn.getresponse()
        if response.status is 200:
            body = response.read()
            return json.loads(body)

        return None
    except Exception as e:
        print(e)
        return None
