import sys
import json

def main(params):
    # tODO error management if not docs or if no return
    if not "docs" in params.keys():
        return json.loads(json.dumps({"error":500}))
    if (params["docs"] == []):
        return json.loads(json.dumps({"error":404}))
    dataList=[]
    for doc in params["docs"]:
        for keyword in ["id","name","dealership","review","purchase","purchase_date","car_make","car_model","car_year"]:
            if not keyword in doc.keys():
                doc[keyword] = ""
        dataList.append({ 
          "id": doc["id"],
          "name": doc["name"],
          "dealership": doc["dealership"],
          "review": doc["review"],
          "purchase": doc["purchase"],      
          "purchase_date": doc["purchase_date"],
          "car_make": doc["car_make"],
          "car_model": doc["car_model"],
          "car_year": doc["car_year"],
        })
    # TODO : error messages management
    return json.loads(json.dumps({"data": dataList}))