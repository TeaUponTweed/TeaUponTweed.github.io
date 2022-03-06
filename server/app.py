from flask import Flask, request, send_from_directory, send_file

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='.')

@app.route("/")
def home():
	return send_file('index.html')

# @app.route('/static/<path:path>')
# def send_static(path):
#     return send_from_directory('./', path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
