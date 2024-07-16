from flask import Flask
import click

from adapter_layer.views.coordinates import get_coordinates_blueprint
from adapter_layer.views.elevation import get_elevation_blueprint
from adapter_layer.views.huts import get_huts_blueprint
from adapter_layer.views.trail_image import get_trail_image_blueprint
from adapter_layer.views.trails import get_trails_blueprint
from adapter_layer.views.weather_forecasts import get_weather_forecasts_blueprint
from adapter_layer.views.weather_icon import get_weather_icon_blueprint
from adapter_layer.views.hut_image import get_hut_image_blueprint

app = Flask(__name__)

app.register_blueprint(get_coordinates_blueprint, url_prefix='/coordinates')
app.register_blueprint(get_elevation_blueprint, url_prefix='/elevation')
app.register_blueprint(get_huts_blueprint, url_prefix='/huts')
app.register_blueprint(get_trail_image_blueprint, url_prefix='/trailimage')
app.register_blueprint(get_trails_blueprint, url_prefix='/trails')
app.register_blueprint(get_weather_forecasts_blueprint, url_prefix='/weatherforecasts')
app.register_blueprint(get_weather_icon_blueprint, url_prefix='/weathericon')
app.register_blueprint(get_hut_image_blueprint, url_prefix='/hutimage')

@app.cli.command('routes')
def print_routes():
    for rule in app.url_map.iter_rules():
        click.echo(f"{rule}")

if __name__ == '__main__':
    app.run(debug=True, port=5050)