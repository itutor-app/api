from flask import Blueprint, jsonify, request, current_app, send_file, make_response, Response
import os
bp = Blueprint('measurement', __name__, static_folder='static')

@bp.route("/")
def home():
    return "Tudo OK"


@bp.route("/graph", methods=["POST"])
def graph():
    data = request.json
    current_app.itutor.Reset()
    if data:
        current_app.itutor.FormatData(data)
    current_app.itutor.GenerateRandomName()
    current_app.itutor.GenerateGraph()
    current_app.itutor.CreatePlotComparison()
    print(current_app.config)
    porcento = f"{current_app.itutor.random_percent*100:.2f}%"
    return jsonify({"graph": f"https://itutor-service-zeifba777q-uc.a.run.app/graph/{current_app.itutor.random_name}-graph", "random_percent": porcento}), 200


@bp.route("/graph/<id>")
def graph_image(id):
    return send_file(f"static/{id}.png", mimetype='image/png')

@bp.route("/graph/delete/<id>", methods=["DELETE"])
def graph_delete(id):
    try:
        os.remove(current_app.itutor.PATH_GRAPH_IMAGE.format(name=id))
        os.remove(current_app.itutor.PATH_CURVE_IMAGE.format(name=id)+".png")
        return '', 204
    except Exception as e:
        print(e)
        return '', 404

@bp.route("/curve/<id>")
def curve_image(id):
    return send_file(f"static/{id}.png", mimetype='image/png')

def init_app(app):
  app.register_blueprint(bp)