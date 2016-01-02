# -*- encoding: utf-8 -*-

#

from flask import Flask, render_template, jsonify

app = Flask(__name__)
app.config.from_object('config')


@app.route("/", methods=("GET",))
def index():
    return render_template("index.html")

@app.route("/contact", methods=("POST",))
def contact():
    return jsonify({"result":"ok"})

if __name__ == '__main__':
    app.run("0.0.0.0", port=8000)
