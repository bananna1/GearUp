from flask import Flask

from coordinates import get_coordinates_blueprint
from elevation import get_elevation_blueprint
from huts import get_huts_blueprint
from trail_image import get_trail_image_blueprint
from trails import get_trails_blueprint
from weather_forecasts import get_weather_forecasts_blueprint
from weather_icon import get_weather_icon_blueprint


app = Flask(__name__)

app.register_blueprint(get_coordinates_blueprint, url_prefix='/coordinates')
app.register_blueprint(get_elevation_blueprint, url_prefix='/elevation')
app.register_blueprint(get_huts_blueprint, url_prefix='/huts')
app.register_blueprint(get_trail_image_blueprint, url_prefix='/trailimage')
app.register_blueprint(get_trails_blueprint, url_prefix='/trails')
app.register_blueprint(get_weather_forecasts_blueprint, url_prefix='/weatherforecasts')
app.register_blueprint(get_weather_icon_blueprint, url_prefix='/weathericon')


if __name__ == "__main__":
    app.run(debug=True, port=5050)