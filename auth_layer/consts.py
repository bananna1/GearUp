GOOGLE_CLIENT_ID = "821867949302-kfjp4anv65esln75vka0tqjig8bq9dsd.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'openid']
REDIRECT_URI = 'http://localhost:5000/auth/callback'
DATA_LAYER_URL = 'http://localhost:5051'
ADD_USER_URL = DATA_LAYER_URL + "/add_user"
GET_USER_URL = DATA_LAYER_URL + "/get_user"