from flask import Flask
from routes import pages
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "c544081efca90d112b80ff0ce139dd98")
app.register_blueprint(pages)

if __name__ == '__main__':
    app.run(debug=True)
