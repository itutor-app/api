from flask import Flask
from extensions.configure import load_extensions
import socket
import os

app = Flask(__name__)
print("Criou o app flask")
load_extensions(app)

if __name__ == "__main__":
  print("Rodou o app, ip:", socket.gethostbyname(socket.gethostname()))
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
