from flask import Flask
from extensions.configure import init_app, load_extensions
import socket
app = Flask(__name__)
print("Criou o app flask")
init_app(app)
load_extensions(app)

if __name__ == "__main__":
  print("Rodou o app, ip", socket.gethostbyname(socket.gethostname()))
  app.run(host="0.0.0.0", port=8080, debug=True)
