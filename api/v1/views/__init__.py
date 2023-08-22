"""Create a first blueprint"""
from flask import Blueprint

"""new instance from Blueprint"""
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

"""wildcard import of everything in the package """
from api.v1.views.index import *