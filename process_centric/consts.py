GOOGLE_CLIENT_ID = "821867949302-kfjp4anv65esln75vka0tqjig8bq9dsd.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GMAPS_API_KEY = "AIzaSyDvxhkd4NAc1iVgZ9h6La8mZpWUL9S5Eqo"


SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'openid']
REDIRECT_URI = 'http://localhost:5000/auth/callback'


GEAR_URL = "http://gear:5004/gear"
WEATHER_URL = "http://weather:5001/weather"
HUTS_URL = "http://huts:5003/huts"
TRAILS_URL = "http://trails:5002/trails"


DATA_LAYER_URL = 'http://data_layer:5051'
ADD_USER_URL = DATA_LAYER_URL + "/add_user/"
GET_USER_URL = DATA_LAYER_URL + "/get_user"
GET_GEAR_URL = DATA_LAYER_URL + "/get_gear/id/"
GET_FAVOURITE_GEAR_URL = DATA_LAYER_URL + '/get_favourite_gear/'
ADD_FAVOURITE_GEAR_URL = DATA_LAYER_URL + '/add_favourite_gear/'
REMOVE_FAVOURITE_GEAR_URL = DATA_LAYER_URL + '/remove_favourite_gear'