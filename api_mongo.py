from flask import Flask, request,jsonify,redirect,url_for
from flask_pymongo import PyMongo
import json

app=Flask(__name__)
app.config['MONGO_DBNAME']='udemy_collect' #project name under cluster0
app.config['MONGO_URI']="mongodb+srv://test:test@cluster0-yro7g.mongodb.net/api_flask?retryWrites=true&w=majority"
#add database name above after .net/
mongo=PyMongo(app)

@app.route("/data",methods=['GET'])
def all_data():
    data=mongo.db.user_data #connect to test collection in mongodb udemy_collect
    output=[]
    for i in data.find():
        output.append({"name":i['name'],"age":i['age']})
    return jsonify({"result":output})

@app.route("/data/<name>",methods=['GET'])
def spec_data(name):
    data=mongo.db.user_data
    q = data.find_one({"name":name})
    if q:
        output={"name":q['name'],"age":q["age"]}
    else:
        output="No result for query " + str(name)
    return jsonify({'result':output})

@app.route("/data",methods=['POST'])
def add_data():
    name=request.json['name']
    age=request.json['age']
    data=mongo.db.user_data
    entery_id=data.insert({'name':name,'age':age})
    get_data=data.find_one({"_id":entery_id})
    output={'name':get_data['name'],'age':get_data['age']}
    return jsonify({'result':output})

@app.route("/data/<name>",methods=['PUT'])
def edit_data(name):
    data=mongo.db.user_data
    q=data.find_one({"name":name})
    if q:
        old={"name":q['name'],"age":q['age']}

        if  'name' in request.json:
            n_name=request.json['name']
        else:
            n_name=q['name']
        if 'age' in request.json:
            n_age=request.json['age']
        else:
            n_age=q['age']
        if n_name or n_age:
            new={"$set":{"name":n_name,"age":n_age}}
            entery_id=data.update_one(old,new)
            return redirect(url_for("all_data"))
    else:
        output="No feild present for " + str(name)
        return jsonify({"result":output})

@app.route("/data/<string:name>",methods=['DELETE'])
def delete_data(name):
    data=mongo.db.user_data
    q=data.find_one({"name":name})
    if q:
        data.delete_one(q)
        return redirect(url_for("all_data"))
    else:
        output="No feild present for " + str(name)
        return jsonify({"result":output})



app.run(host='192.168.1.104',debug=True)