from flask_app import app
from flask_app.controllers import users,songs
import os

app.secret_key = os.environ.get("SECRET_KEY")

if __name__ == "__main__":
    app.run(debug= True)