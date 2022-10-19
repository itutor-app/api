from flask import Flask
from itutor.extensions.configure import init_app, load_extensions

app = Flask(__name__)
print("Criou o app flask")
init_app(app)
load_extensions(app)

if __name__ == "__main__":
  print("Rodou o app")
  app.run(host="0.0.0.0", port=443)
