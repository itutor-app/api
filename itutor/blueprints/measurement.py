from flask import Blueprint, jsonify, request, current_app, send_file, make_response, Response
import os


bp = Blueprint('measurement', __name__, static_folder='static')
@bp.route("/")
def home():
    return "Tudo OK"


@bp.route("/graph", methods=["POST"])
def graph_generate():
    data = request.json
    current_app.itutor.Reset()
    if data:
        current_app.itutor.FormatData(data)
        current_app.itutor.SetName(data[0]["discussion_id"])
        current_app.itutor.GenerateGraph()
        current_app.itutor.CreatePlotComparison()

        porcento = f"{current_app.itutor.random_percent*100:.2f}%"
        return jsonify({"graph": f"{request.base_url}/{current_app.itutor.random_name}",
                        "random_percent": porcento,
                        "id": current_app.itutor.random_name}),\
                        200
    return "Empty data", 400

@bp.route("/graph/<id>", methods=["GET"])
def graph_image(id):
    try:
        return send_file(f"{current_app.itutor.PATH_GRAPH_IMAGE.format(name=id)}", mimetype='image/png')
    except:
        return '', 404
        
@bp.route("/graph/<id>", methods=["DELETE"])
def graph_delete(id):
    try:
        os.remove(current_app.itutor.PATH_GRAPH_IMAGE.format(name=id))
        os.remove(current_app.itutor.PATH_HIST_IMAGE.format(name=id) + ".png")
        return '', 204
    except Exception as e:
        print(e)
        return '', 404

@bp.route("/curve/<id>")
def curve_image(id):
    return send_file(f"{current_app.itutor.PATH_HIST_IMAGE.format(name=id)}", mimetype='image/png')

@bp.route("/delete-all", methods=["DELETE"])
def delete_all():
    for file in os.listdir(current_app.itutor.STATIC_PATH):
        os.remove(current_app.itutor.STATIC_PATH+"/"+file)
    return "", 204


def init_app(app):
  app.register_blueprint(bp)