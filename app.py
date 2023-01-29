import falcon
from services import Refresh_Data, Retrieve_Data, Version

api = application = falcon.API()
api.add_route("/version", Version())
api.add_route("/refresh-data", Refresh_Data())
api.add_route("/retrieve-data", Retrieve_Data())
