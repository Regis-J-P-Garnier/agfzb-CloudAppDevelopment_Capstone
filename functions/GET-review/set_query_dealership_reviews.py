import sys
import json

def main(params):
    if not "dealerId" in params.keys():
        params["dealerId"]=0
    params["dealerId"]=int(params["dealerId"])
    returnDict={
        "include_docs": True,
        "database":"reviews",
        "query":{
               "selector": {
                  "dealership": {
                     "$eq": params["dealerId"]
                  }
               },
               "fields": [
                  "id",
                  "dealership",
                  "review",
                  "name",
                  "purchase",
                  "purchase_date",
                  "car_make",
                  "car_model",
                  "car_year",
               ],
               "sort": [
                  {
                     "dealership": "asc",
                  }
               ]
            }, 
        "params": {},
    }
    return json.loads(json.dumps(returnDict))