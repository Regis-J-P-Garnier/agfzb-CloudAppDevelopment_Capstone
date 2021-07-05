import sys
import json

def main(params):
    if not ("ok" in params.keys()):
        return json.loads(json.dumps({"error":500}))
    if not (params["ok"] == True):
        return json.loads(json.dumps({"error":500}))
    else: 
        return json.loads(json.dumps({"data":params}))