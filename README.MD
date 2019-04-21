### Install
- Clone repository
- docker-compose build
- docker-composer up

### Important
- web/app.py.
- For test "production server" use ec2-35-165-231-168.us-west-2.compute.amazonaws.com:5000/ instead of http://0.0.0.0:5000/

### Create League
- In Postman send as { "league_name" : "Kanto"} // JSON(application/json) // POST
- http://0.0.0.0:5000/leagues to create a League.

### Create Trainer
- In Postman send as { "league_name" : "Kanto", "trainer_name" : "Alejandro", "pokemons_number" : 6} // JSON(application/json) // POST
- http://0.0.0.0:5000/trainers to create a League.

### Dump pokemons saved in DB
- http://0.0.0.0:5000/dbpokemons
