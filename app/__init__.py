from flask import Flask
from app import config

# Initialisze l'application Flask
app = Flask( __name__ )

from app import views

from app import models
from app import config

