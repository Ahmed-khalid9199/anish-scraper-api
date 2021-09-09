import flask
from flask import request, jsonify
from flask_cors import CORS
from vivago import vivago

app = flask.Flask(__name__)
CORS(app= app)

app.config["DEBUG"]= True


@app.route("/", methods=['POST'])
def get_tickets():
    link = request.form['url']
    print(request)
    print(request.form)
    data_list = list()
    if 'www.viagogo.com' in link:
        data_list = vivago(link)

    if data_list:
        return jsonify(data_list)
    else:
        return jsonify({"msg": "something wrong"})


@app.route("/home")
def home_view():
        return "<h1>Welcome to API</h1>"


if __name__ == "__main__":
    app.run()