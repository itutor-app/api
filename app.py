from flask import Flask, request, jsonify, send_file
import ITutor

app = Flask(__name__)


@app.route("/graph", methods=["POST"])
def graph():
    data = request.json
    app.itutor.start()
    print(data)
    return jsonify({"graph": "http://127.0.0.1:5000/graph/image", "curve": "http://127.0.0.1:5000/curve/image"}), 200


@app.route("/graph/image")
def graph_image():
    return send_file("static/grafos/Graph.png", mimetype='image/png')


@app.route("/curve/image")
def curve_image():
    return send_file("static/curvas/Curves-Comparison.png", mimetype='image/png')


if __name__ == "__main__":
    app.itutor = ITutor.ITutorClassificator()
    app.run()
