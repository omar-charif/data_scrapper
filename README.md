# data_scrapper
webpage data scrapper

# Description
This tool scrape exports data from a webpage and load them into SQlite database.
it is then converted to a restful API.

# usage
## deploy rest api locally using docker
- Pull latest image from docker hub: docker pull ocharif/data-scrapper:latest
- Run docker container: docker run -it ocharif/data-scrapper:latest

REST API has two endpoints:
- version: serve as healthcheck and return the version of backend app. It can be reached at: http://127.0.0.1:5050/version
- retrieve-data: retrieve data from data base. It can be reached at: http://127.0.0.1:5050/retrieve-data