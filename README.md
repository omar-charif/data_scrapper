# data_scrapper
webpage data scrapper

# Description
This tool scrape exports data from a webpage and load them into SQlite database.
it is then converted to a restful API.

# usage
## deploy rest api locally using docker-compose
- Build docker image by running: docker-compose build
- Run docker container and deploy rest api locally: docker-compose up

REST API has two endpoints:
- version: serve as healthcheck and return the version of backend app. It can be reached at: http://127.0.0.1:5050/version
- retrieve-data: retrieve data from data base. It can be reached at: http://127.0.0.1:5050/retrieve-data