from pymongo import MongoClient
from flask import Flask, jsonify, request 
import json
from datetime import datetime
from flask import send_file
import qrcodegen



# client = MongoClient('mongodb+srv://ai-drone:oOIUq8IGcTVKy7JV@cluster0-igbga.mongodb.net/test?retryWrites=true&w=majority',27017)
client=MongoClient('localhost',27017)
db=client.test
col=db.user
col1=db.drone
col2=db.inventory
col3=db.order




app = Flask(__name__) 
  
# on the terminal type: curl http://127.0.0.1:5000/ 
# returns hello world when we use GET. 
# returns the data that we send when we use POST. 
@app.route('/signup', methods = ["POST"]) 
def signup():
    data=request.json
    id=data['id']
    name=str(data['name'])
    email=str(data['email'])
    password=str(data['password'])
    for x in col.find():
        print(x)
    print(col.find_one({"email": email}))
    if(col.find_one({"email": email})):
        print(col.find_one({"email": email}))
        return "Already Registered"
    else:
        col.insert({ "id":id, "name": name, "email":email, "password":password},check_keys=False)
    return "Inserted"
    
@app.route('/adddrone', methods = ["POST"]) 
def adddrone():
    data=request.json
    id=data['id']
    name=str(data['name'])
    capacity=data['capacity']
    availability=str(data['availability'])
    if(col1.find_one({"name": name})):
        print(col1.find_one({"name": name}))
        return "Drone already registered"
    else:
        col1.insert({ "id":id, "name": name, "capacity":capacity, "availability":availability},check_keys=False)
    return "Inserted"

@app.route('/getdrones', methods = ["GET"]) 
def getdrones():
    response = []
    documents=col1.find()
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    return json.dumps(response)

@app.route('/updateavailability', methods = ["PUT"]) 
def updateavailability():
    data=request.json
    name=data['name']
    availability=data['availability']
    myquery = { "name": name }
    newvalues = { "$set": { "availability": availability } }
    col1.update_one(myquery, newvalues)
    if(col1.find_one({"name":name})):
        return "Updated"
    else:
        return "No such Drone"
@app.route('/addinventory', methods = ["POST"]) 
def addinventory():
    data=request.json
    id=data['id']
    name=str(data['name'])
    units=data['units']
    if(units>0):
        availability=True
    else:
        availability=False
    weight=data['weight']
    if(col2.find_one({"name": name})):
        print(col2.find_one({"name": name}))
        return "Inventory item already present"
    else:
        col2.insert({ "id":id, "name": name, "units":units, "availability":availability,"weight":weight},check_keys=False)
    return "Inserted"
@app.route('/fetchinventory', methods = ["GET"]) 
def fetchinventory():
    response = []
    documents=col2.find()
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    return json.dumps(response)
@app.route('/updateunits', methods = ["PUT"]) 
def updateunits():
    data=request.json
    name=data['name']
    units=data['units']
    myquery = { "name": name }
    newvalues = { "$set": { "units": units } }
    col2.update_one(myquery, newvalues)
    if(units==0):
        myquery = { "name": name }
        newvalues = { "$set": { "availability": False } }
        col2.update_one(myquery, newvalues)
    else:
        myquery = { "name": name }
        newvalues = { "$set": { "availability": True } }
        col2.update_one(myquery, newvalues)
    if(col2.find_one({"name":name})):
        return "Updated units"
    else:
        return "No such item found"
@app.route('/addorder', methods = ["POST"]) 
def addorder():
    data=request.json
    id=data['id']
    quantity=data['quantity']
    dateTimeObj = datetime.now()
    timestamp=dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    if(col3.find_one({"id": id})):
        print(col3.find_one({"id": id}))
        return "Order with same ID is present"
    else:
        col3.insert({ "id":id, "quantity": quantity, "timestamp":timestamp},check_keys=False)
    return "Order added"
@app.route('/fetchorders', methods = ["GET"]) 
def fetchorders():
    response = []
    documents=col3.find()
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    return json.dumps(response)

@app.route('/get_image')
def get_image():
    qrcodegen.genqrcode()
    if request.args.get('type') == '1':
       filename = 'code.jpg'
    else:
       filename = 'code.jpg'
    return send_file(filename, mimetype='image/gif')
if __name__ == '__main__': 
  
    app.run(debug = True) 