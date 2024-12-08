from os import environ
from Metrocar import app  # Import the app from Metrocar/__init__.py
from Metrocar.views import views_blueprint  # Import the blueprint

# Register the blueprint with the app
app.register_blueprint(views_blueprint, url_prefix='/')



if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
