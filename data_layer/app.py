from app import app
import click

@app.cli.command('routes')
def print_routes():
    for rule in app.url_map.iter_rules():
        click.echo(f"{rule}")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5051, debug=True)
