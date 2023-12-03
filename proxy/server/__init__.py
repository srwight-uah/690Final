from flask import Flask, g
from typing import List, Dict

GET, PUT, POST, DELETE = ('GET',), ('PUT',), ('POST',), ('DELETE')

app = Flask(__name__)

from . import routes
print('routes imported')