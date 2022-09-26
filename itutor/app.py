from flask import Flask
from itutor.extensions.configure import init_app, load_extensions

app = Flask(__name__)

init_app(app)
load_extensions(app)

if __name__ == "__main__":
  app.run()
