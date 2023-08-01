#!/usr/bin/python3
"""
This module contains the principal application
"""

from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
import os
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


# Declare a method to handle app.teardown_appcontext that calls storage.close()
@app.teardown_appcontext
def close_storage(exception):
    """Closes the database storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return make_response(jsonify({"error": "Not found"}), 404)


app.config['SWAGGER'] = {
    'title': 'AirBnB clone - RESTful API',
    'description': 'This is the api that was created for the hbnb restful \
    api project, all the documentation will be shown below',
    'uiversion': 3}

Swagger(app)


# Inside if __name__ == "__main__":, run your Flask server (variable app)
if __name__ == "__main__":
    # Set the host and port based on environment variables or use defaults
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))

    # Run the Flask server
    app.run(host=host, port=port, threaded=True)
