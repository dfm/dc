import os

e = os.environ

DEBUG      = e.get("DEBUG", "n").lower() == "y"
SECRET_KEY = e.get("SECRET_KEY", "develop")
MONGOLAB_URI = e["MONGOLAB_URI"]

