from blueprints.measurement import init_app as init_blueprint
from extensions.itutor_app import init_app as init_itutor

def load_extensions(app):
  init_blueprint(app)
  init_itutor(app)