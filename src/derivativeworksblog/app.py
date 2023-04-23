from flask import Flask, request, send_file, send_from_directory

# set the project root directory as the static folder, you can set others.
app = Flask(__name__)


@app.route("/favicon.ico")
def favicon():
    return send_file("static/favicon.ico")


@app.route("/")
def home():
    return send_file("static/index.html")


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


@app.route("/feed")
def feed():
    return send_file("static/rss.xml")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
