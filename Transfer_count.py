import requests
import json
import datetime
import graphene
from pandas import json_normalize 
import pandas as pd





def run_query(query,variables):  # A simple function to use requests.post to make the API call.
    headers = {'X-API-KEY': 'BQYNgVsDxTS6VcEBf0mRhBYKtwZcwi3t'}
    request = requests.post('https://graphql.bitquery.io/',
                            json={'query': query,'variables': variables}, headers=headers)
    
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed and return code is {}.      {}'.format(request.status_code,
                        query))


# The GraphQL query
variabledict = {}

token = "0x5e90253fbae4dab78aa351f4e6fed08a64ab5590"
limit = 10
offset = 0
network = "bsc"
date_from = datetime.datetime(2021,5,16,0).isoformat()+"Z"
#date_till = datetime.datetime(2021,5,13,15).isoformat()+"Z"
date_till = datetime.datetime.now().isoformat()+"Z"

variabledict["token"] = token
variabledict["limit"] = limit
variabledict["network"] = network
variabledict["offset"] = offset
variabledict["from"] = date_from
variabledict["till"] = date_till

variables = json.dumps(variabledict)



query = """
query ($network: EthereumNetwork!,
                              $token: String!,
                              $from: ISO8601DateTime,
                              $till: ISO8601DateTime){
                          ethereum(network: $network){
                            transfers(currency: {is: $token}
                            amount: {gt: 0}
                            date: {since: $from till: $till}
                            ){

                              currency{
                                symbol
                              }

                              median: amount(calculate: median)
                              average: amount(calculate: average)

                              amount
                              count

                              days: count(uniq: dates)

                              sender_count: count(uniq: senders)
                              receiver_count: count(uniq: receivers)

                              min_date:minimum(of: date)
                              max_date:maximum(of: date)
                            }
                          }
                        }
"""
def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values
    
   

#Main
result = run_query(query,variables = variables)  # Execute the query
data = json_extract(result, "count")

print(f"transfer count milli {date_from} og {date_till} er {data}")

