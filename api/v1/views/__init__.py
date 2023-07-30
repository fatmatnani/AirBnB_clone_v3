#!/usr/bin/python3
"""Init file for views module"""

from flask import Blueprint

# Create a variable app_views which is an instance of Blueprint
# The url_prefix is set to '/api/v1' as specified
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import of everything in the package api.v1.views.index
# PEP8 will complain about it, but don’t worry, it’s normal and this file won’t be checked.
from api.v1.views.index import *
