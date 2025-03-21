import os
import sys
from flask import Flask, jsonify, request
from discord_interactions import verify_key_decorator
from asgiref.wsgi import WsgiToAsgi
from mangum import Mangum

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import PUBLIC_KEY


