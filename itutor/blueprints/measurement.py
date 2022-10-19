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
    current_app.itutor.GenerateGraph()
    current_app.itutor.CreatePlotComparison()
    current_app.itutor.Reset()
    return jsonify({"graph": "https://itutor-api.herokuapp.com/graph/image", "curve": "https://itutor-api.herokuapp.com/curve/image"}), 200


@bp.route("/graph/image")
def graph_image():
    return send_file("static/grafos/Graph.png", mimetype='image/png')


@bp.route("/curve/image")
def curve_image():
    return send_file("static/curvas/Curves-Comparison.png", mimetype='image/png')

def init_app(app):
  app.register_blueprint(bp)