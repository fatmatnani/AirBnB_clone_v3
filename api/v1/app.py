#!/usr/bin/python3
"""
This module contains the principal application
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

# Create a variable app, an instance of Flask
app = Flask(__name__)

# Register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)


# Declare a method to handle app.teardown_appcontext that calls storage.close()

@app.teardown_appcontext
def close_storage(exception):
    """Closes the database storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return (jsonify({"error": "Not found"}), 404)


# Inside if __name__ == "__main__":, run your Flask server (variable app)
if __name__ == "__main__":
    # Set the host and port based on environment variables or use defaults
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))

    # Run the Flask server
    app.run(host=host, port=port, threaded=True)
