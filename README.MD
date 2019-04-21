### Instalación
- Clone repository
- docker-compose build
- docker-composer up

### Important
- web/app.py.
- For test "production server" use ec2-35-165-231-168.us-west-2.compute.amazonaws.com:5000/ instead of http://0.0.0.0:5000/

### Create League
- In Postman send as { "league_name" : "Kanto"} // JSON(application/json)
- http://0.0.0.0:5000/leagues to create a League.
