from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.pokemonleagues
leagues = db["leagues"]
trainers = db["trainers"]
pokemons = db["pokemons"]

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
                "msg" : "Invalid league name."
            }
            return jsonify(retJson)
        
        leagues.insert({
            "league_name" : league_name,
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
        trainer_name = postedData["trainer_name"]
        pokemons_number = postedData["pokemons_number"]

        retJson, error = verifyLeagueName(league_name)
        if error:
            return jsonify(retJson)

        if pokemons_number < 1 or pokemons_number > 6:
            return jsonify(generateReturnDictionary(301, "Invalid pokemons number."))
        
        if trainers.find({"trainer_name": trainer_name}).count() == 0:
            return jsonify(generateReturnDictionary(301, "Trainer is already in a league."))

        trainers.insert({
            "league_name" : league_name,
            "trainer_name" : trainer_name,
            "pokemons_number" : pokemons_number
        })

        count = 0
        for count in range(pokemons_number):
            count += 1
            pokemons.insert({
                "pokemon_name" : "pokemon "+str(count),
                "trainer_name" : trainer_name
            })

        retJson = {
            "status" : 200,
            "msg" : "You add trainer to league succesfully."
        }
        return jsonify(retJson)

api.add_resource(League, '/leagues')
api.add_resource(Trainer, '/trainers')

@app.route("/allleagues")
def getLeagues():
    return dumps(leagues.find())
    
@app.route("/allpokemons")
def getPokemons():
    return dumps(pokemons.find())

@app.route("/alltrainers")
def getTrainers():
    return dumps(trainers.find())

if __name__ == "__main__":
    app.run(host='0.0.0.0')
        



        

    



