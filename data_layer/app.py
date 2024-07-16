from app import app
import click

@app.cli.command('routes')
def print_routes():
    for rule in app.url_map.iter_rules():
        click.echo(f"{rule}")

if __name__ == '__main__':
    app.run(debug=True, port=5051)
