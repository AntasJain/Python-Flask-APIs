from flask import Flask, request
from db import items,stores
from flask_smorest import abort
import uuid
app = Flask(__name__)



@app.get("/store") #http://127.0.0.1:5000/store
def get_stores():
    return {"stores":list(stores.values())}

@app.post("/store")
def create_stores():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400,message="name must be included in the payload")
    for store in stores.values():
        if store_data["name"]==store["name"]:
            abort(400,message="Store already Exists")
    store_id = uuid.uuid4().hex
    store = {**store_data,'id':store_id}
    stores[store_id]=store
    return store,201

@app.post("/item")
def create_item(name):
    item_data = request.get_json()
    if('price' not in item_data or 'store_id' not in item_data or 'name' not in item_data):
        abort(400,message="bad request. Ensure 'price', 'store_id' and 'name' are included in the JSON playload")
    if(item_data["store_id"] not in stores):
        abort(404, message="Store not found")
    for item in items.values():
        if item_data["name"]==item["name"] and item_data["store_id"]==item["store_id"]:
           abort(400,message="Item already exist") 
    item_id = uuid.uuid4().hex
    item = {**item_data,'id':item_id}
    items[item_id]=item
    return item,201
    
@app.get("/items")
def get_all_items():
       return {"items":list(items.values())} 

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id],201
    except KeyError:
        abort(404,message="Store not found")
    

@app.get("/item/<string:item_id>")
def get_store_items(item_id):
    try:
        return items[item_id],201
    except KeyError:
        abort(404,message="item not found")