### Install
- Clone repository
- docker-compose build
- docker-composer up

### Important
- web/app.py.
- For test "production server" use ec2-35-165-231-168.us-west-2.compute.amazonaws.com:5000/ instead of http://0.0.0.0:5000/

### Create League
- In Postman send as { "league_name" : "Kanto"} // JSON(application/json) // POST
- Condition: The league name must be unique.
- http://0.0.0.0:5000/leagues to create a League.

### Create Trainer
- In Postman send as { "league_name" : "Kanto", "trainer_name" : "Alejandro", "pokemons_number" : 6} // JSON(application/json) // POST
- Conditions: 
- The league name must be exist.
- Pokemons number between 1 and 6.
- Trainer must not be registered in another league.
- Pokemons are added according to the pokemons_number.
- http://0.0.0.0:5000/trainers to create a Trainer.

### Battle
- In Postman send as { "league_name" : "Kanto", "first_trainer_name" : "Alejandro", "second_trainer_name" : "Adriana"} // JSON(application/json) // POST
- Conditions:
- The league name must be exist.
- Trainer names must exist.
- Trainers must be different.
- Trainers must be in the league.
- The trainer who has the most pokemons wins.
- http://0.0.0.0:5000/battle to play a battle.

### Positions order by Victories DESC/ METHOD GET
- http://0.0.0.0:5000/positions/victories

### Positions order by Defeats DESC/ METHOD GET
- http://0.0.0.0:5000/positions/defeats

### Dump pokemons saved in DB / METHOD GET
- http://0.0.0.0:5000/dbpokemons

### Dump trainers saved in DB / METHOD GET
- http://0.0.0.0:5000/dbtrainers

### Dump leagues saved in DB / METHOD GET
- http://0.0.0.0:5000/dbleagues
