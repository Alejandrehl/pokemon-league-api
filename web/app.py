from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from bson.json_util import dumps
import pokebase as pb
import requests as req
import json
import collections
import secrets

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.pokemonleagues
leagues = db["leagues"]
trainers = db["trainers"]
pokemons = db["pokemons"]
positions = db["positions"]

def getPokemons():
    url = "https://pokeapi.co/api/v2/pokemon"
    data = req.get(url).json()
    return data["results"]

def leagueExist(league_name):
    if leagues.find({"league_name": league_name}).count() == 0:
        return False
    else:
        return True

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
        
        if not trainers.find({"trainer_name": trainer_name}).count() == 0:
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
                "pokemon_name" : secrets.choice(list(getPokemons()))['name'],
                "trainer_name" : trainer_name
            })

        retJson = {
            "status" : 200,
            "msg" : "You add trainer to league succesfully."
        }
        return jsonify(retJson)

class Battle(Resource):
    def post(self):
        postedData = request.get_json()
        league_name = postedData["league_name"]
        first_trainer_name = postedData["first_trainer_name"]
        second_trainer_name = postedData["second_trainer_name"]

        retJson, error = verifyLeagueName(league_name)
        if error:
            return jsonify(retJson)

        if trainers.find({"trainer_name": first_trainer_name}).count() == 0:
            return jsonify(generateReturnDictionary(301, "First Trainer is invalid."))
        else: 
            trainer = trainers.find({"trainer_name": first_trainer_name})
            if not trainer[0]["league_name"] == league_name:
                return jsonify(generateReturnDictionary(301, "First trainer is not in this league."))

        if trainers.find({"trainer_name": second_trainer_name}).count() == 0:
            return jsonify(generateReturnDictionary(301, "SecondTrainer is invalid."))
        else: 
            trainer = trainers.find({"trainer_name": second_trainer_name})
            if not trainer[0]["league_name"] == league_name:
                return jsonify(generateReturnDictionary(301, "Second trainer is not in this league."))
        
        if first_trainer_name == second_trainer_name:
            return jsonify(generateReturnDictionary(301, "The trainers must be different."))

        first_trainer_pokemons = pokemons.find({ "trainer_name" : first_trainer_name})
        second_trainer_pokemons = pokemons.find({ "trainer_name" : second_trainer_name})

        if first_trainer_pokemons.count() == second_trainer_pokemons.count():
            return jsonify(generateReturnDictionary(200, "¡WoW! The trainers have tied."))
        else: 
            if first_trainer_pokemons.count() > second_trainer_pokemons.count():
                winner_name = first_trainer_name
                loser_name = second_trainer_name
            else:
                winner_name = second_trainer_name
                loser_name = first_trainer_name

        if positions.find({"trainer_name": winner_name}).count() == 0:
            positions.insert({
                "trainer_name" : winner_name,
                "victories" : 1,
                "defeats" : 0
            })
        else:
            positions.update({
                "trainer_name" : winner_name
            }, {
                "$set" : {
                    "victories" : positions.find({"trainer_name": winner_name})[0]["victories"] + 1
                }
            })

        if positions.find({"trainer_name": loser_name}).count() == 0:
            positions.insert({
                "trainer_name" : loser_name,
                "victories" : 0,
                "defeats" : 1
            })
        else:
            positions.update({
                "trainer_name" : loser_name
            }, {
                "$set" : {
                    "defeats" : positions.find({"trainer_name": loser_name})[0]["defeats"] + 1
                }
            })

        return jsonify(generateReturnDictionary(200, "WoW! The trainer "+winner_name+" has won."))

class Training(Resource):
    def post(self):
        postedData = request.get_json()
        first_trainer_name = postedData["first_trainer_name"]
        second_trainer_name = postedData["second_trainer_name"]

        if trainers.find({"trainer_name": first_trainer_name}).count() == 0:
            return jsonify(generateReturnDictionary(301, "First Trainer is invalid."))

        if trainers.find({"trainer_name": second_trainer_name}).count() == 0:
            return jsonify(generateReturnDictionary(301, "SecondTrainer is invalid."))
        
        if first_trainer_name == second_trainer_name:
            return jsonify(generateReturnDictionary(301, "The trainers must be different."))

        first_trainer_pokemons = pokemons.find({ "trainer_name" : first_trainer_name})
        second_trainer_pokemons = pokemons.find({ "trainer_name" : second_trainer_name})

        if first_trainer_pokemons.count() == second_trainer_pokemons.count():
            return jsonify(generateReturnDictionary(200, "¡WoW! The trainers have tied."))
        else: 
            if first_trainer_pokemons.count() > second_trainer_pokemons.count():
                winner_name = first_trainer_name
                loser_name = second_trainer_name
            else:
                winner_name = second_trainer_name
                loser_name = first_trainer_name

        return jsonify(generateReturnDictionary(200, "WoW! The trainer "+winner_name+" has won the traning."))

class LeagueWinner(Resource):
    def post(self):
        postedData = request.get_json()
        league_name = postedData["league_name"]

        retJson, error = verifyLeagueName(league_name)
        if error:
            return jsonify(retJson)
        
        league_trainers = trainers.find({"league_name" : league_name})
        count = 0
        best_trainer = False
        for count in range(league_trainers.count()):
            actual_trainer = positions.find({ "trainer_name" : league_trainers[count]["trainer_name"]})
    
            if best_trainer == False:
                best_trainer = actual_trainer
            else:
                if best_trainer[0]["victories"] < actual_trainer[0]["victories"]:
                    best_trainer = actual_trainer
            
            count += 1

        return dumps(best_trainer)
            


api.add_resource(League, '/leagues')
api.add_resource(Trainer, '/trainers')
api.add_resource(Battle, '/battle')
api.add_resource(Training, '/training')
api.add_resource(LeagueWinner, '/leaguewinner')

@app.route("/positions/victories")
def victories():
    dbPositions = positions.find().sort("victories", -1)
    return dumps(dbPositions)

@app.route("/positions/defeats")
def defeats():
    dbPositions = positions.find().sort("defeats", -1)
    return dumps(dbPositions)

@app.route("/dbpokemons")
def dbPokemons():
    return dumps(pokemons.find())

@app.route("/dbleagues")
def dbLeagues():
    return dumps(leagues.find())

@app.route("/dbtrainers")
def dbTrainers():
    return dumps(trainers.find())

if __name__ == "__main__":
    app.run(host='0.0.0.0')
        



        

    



