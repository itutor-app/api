from flask import Blueprint, jsonify, request, current_app, send_file

bp = Blueprint('measurement', __name__, static_folder='static')

@bp.route("/")
def home():
    return "Tudo OK"


@bp.route("/graph", methods=["POST"])
def graph():
    data = request.json

    if data:
        current_app.itutor.FormatData(data)

    current_app.itutor.Reset()
    current_app.itutor.GenerateRandomName()
    current_app.itutor.GenerateGraph()
    current_app.itutor.CreatePlotComparison()

    return jsonify({"graph": f"https://itutor-api.herokuapp.com/graph/{current_app.itutor.random_name}-graph", "random_percent": current_app.itutor.random_percent}), 200


@bp.route("/graph/<id>")
def graph_image(id):
    return send_file(f"static/grafos/{id}.png", mimetype='image/png')


@bp.route("/curve/<id>")
def curve_image(id):
    return send_file(f"static/curvas/{id}.png", mimetype='image/png')

def init_app(app):
  app.register_blueprint(bp)