import requests
import json

# rest api --> web api

# requests.get()  # library api

#endpoint = "https://httpbin.org/anything"
# url = "http://127.0.0.1:8000/stuinfo/"
# url = "http://127.0.0.1:8000/stucreate/"
# url = "http://127.0.0.1:8000/studentapi/"
url = "http://127.0.0.1:8000/studentapicls/"

# for post request
"""data = {
    'name':'Jyoti',
    'roll': 101,
    'city': 'Delhi',
    'f':1
}"""

# get request
def get_data(id=None):
    data = {}
    if id is not None:
        data = {'id':id}
    json_data = json.dumps(data)
    r = requests.get(url=url,data=json_data)
    print(r.json())
#get_data(2)

# post request
def post_data():

    data = {
    'name':'reeru',
    'roll': 100,
    'city': 'ranchi',}

    json_data = json.dumps(data) # converting python dictionary into json
    r = requests.post(url=url,data=json_data)
    print(r.json())

post_data()

# update request
def update_data():

    data = {
    'id': 85,
    'name': 'Jyoti',
    'roll': 106,
    'city': 'Delhi',}

    json_data = json.dumps(data) # converting python dictionary into json
    r = requests.put(url=url,data=json_data)
    print(r.json())

#update_data()


# deleting data
def delete_data():

    data = {
    'id': 64 }

    json_data = json.dumps(data) # converting python dictionary into json
    r = requests.delete(url=url,data=json_data)
    print(r.json())


#delete_data()

#print(help(requests.get))
#print(help(requests.post))
# response = requests.get(url) # http request, # params are query parameters
#json_data = json.dumps(data)
#response = requests.post(url=url,data=json_data)
# print((response.text)) # print raw text response
# http request --> HTML
# rest api http request -->  JSON, sometimes in xml also
# Javascript object notation --> almost a python dictionary
# print(dir(response))
#print(response.json()) # print json response
#print(response.status_code) # return status code of the request

