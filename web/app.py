from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.pokemonleagues
leagues = db["leagues"]

def leagueExist(league_name):
    if leagues.find({"league_name": league_name}).count() == 0:
        return False
    else:
        return True

class League(Resource):
    def post(self):
        postedData = request.get_json()
        league_name = postedData["name"]

        if leagueExist(league_name):
            retJson = {
                "status" : 301,
                "msg" : "Invalid username"
            }
            return jsonify(retJson)
        
        leagues.insert({
            "league_name" : league_name
        })

        retJson = {
            "status" : 200,
            "msg" : "You succesfully signed up for the API"
        }

        return jsonify(retJson)

api.add_resource(League, '/leagues')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
        



        

    



