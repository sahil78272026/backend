import requests
import json

# rest api --> web api

# requests.get()  # library api

#endpoint = "https://httpbin.org/anything"
# url = "http://127.0.0.1:8000/stuinfo/"
# url = "http://127.0.0.1:8000/stucreate/"
# url = "http://127.0.0.1:8000/studentapi/"
# url = "http://127.0.0.1:8000/studentapicls/"
url = "http://127.0.0.1:8000/classbasedstudent_api_with_view/85"
url = "http://127.0.0.1:8000/classbasedcloth_api_with_view/"


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
    headers={
        'content-Type':'application/json'
    }
    json_data = json.dumps(data)
    r = requests.get(url=url, headers=headers, data=json_data)
    print(r.json())

get_data(85)

# post request
def post_data():

    data = {
    'name':'newEmmp',
    'roll': 102,
    'city': 'ranchi',}

    # for cloth object
    data={
        'brand_name':"Lewis",
        'fabric': 'cotton',
        'sku': '01',
        'fitting_type': 'male',
        'imported': True,
        'category_id': 'small'
    }

    headers={
        'content-Type':'application/json'
    }

    json_data = json.dumps(data) # converting python dictionary into json
    r = requests.post(url=url, headers=headers, data=json_data)
    print(r.json())

#post_data()

# update request
def update_data():

    data = {
    'id': 1,
    'name': 'Jyoti',
    'roll': 106,
    'city': 'Delhi',}

    headers={
        'content-Type':'application/json'
    }

    json_data = json.dumps(data) # converting python dictionary into json
    r = requests.put(url=url, headers=headers, data=json_data)
    print(r.json())

# update_data()


# deleting data
def delete_data(id):

    data = {
    'id': id }

    headers={
        'content-Type':'application/json'
    }

    json_data = json.dumps(data) # converting python dictionary into json
    r = requests.delete(url=url, headers=headers, data=json_data)
    print(r.json())


# delete_data(2)

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

