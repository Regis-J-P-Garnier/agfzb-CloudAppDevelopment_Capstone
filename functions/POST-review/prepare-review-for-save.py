import sys
import json

def main(params):
    if (params["dealership"] and params["dealership"] != "" and params["name"] and params["name"] != "" and params["review"] and params["review"] != ""):
        dealershipID = int(params["dealership"])
        if (params["purchase"] == "True" or params["purchase"] == "true" or params["purchase"]==True):
            purchaseBool = True
        else:
            purchaseBool = False
        if not "another" in params.keys():
            params["another"] = ""
        if not "purchase_date" in params.keys():
            params["purchase_date"] =""
        if not "car_make" in params.keys():
            params["car_make"] =""
        if not "car_model" in params.keys():
            params["car_model"] =""
        if not "car_year" in params.keys():
            params["car_year"] =""
        returnDict={"doc":
                {   "dealership": dealershipID,
                    "purchase": purchaseBool,
                    "name": params["name"],
                    "review": params["review"],
                    "another": params["another"],
                    "purchase_date": params["purchase_date"],
                    "car_make": params["car_make"],
                    "car_model": params["car_model"],
                    "car_year": params["car_year"],
                }
        }
        return json.loads(json.dumps(returnDict))
    else:
        return { "error": 'no dealership, name or review'}