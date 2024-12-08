
from flask import Flask

# Initialize Flask app
app = Flask(__name__)

# Import views and models after app initialization
import Metrocar.views