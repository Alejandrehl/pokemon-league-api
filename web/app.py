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
        league_name = postedData["league_name"]

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
            "msg" : "You created a League succesfully"
        }

        return jsonify(retJson)

def generateReturnDictionary(status, msg):
    retJson = {
        "status" : status,
        "msg" : msg
    }
    return retJson

def verifyLeagueName(league_name):
    if not leagueExist(league_name):
        return generateReturnDictionary(301, "Invalid league name."), True

    return None, False

class Trainer(Resource):
    def post(self):
        postedData = request.get_json()
        league_name = postedData["league_name"]
        pokemons_number = postedData["pokemons_number"]

        retJson, error = verifyLeagueName(league_name)
        if error:
            return jsonify(retJson)

        if pokemons_number < 1 or pokemons_number > 6:
            return jsonify(generateReturnDictionary(301, "Invalid pokemons number."))
        
        return jsonify(pokemons_number)

api.add_resource(League, '/leagues')
api.add_resource(Trainer, '/trainers')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
        



        

    



