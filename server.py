#! /usr/bin/env python3
from flask import Flask, render_template, url_for, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

autor1 = {
    "nombre": "Walter",
    "apellido": "Mendoza"
    }

autor2 = {
    "nombre": "Byron",
    "apellido": "López"
    }

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cargar_imagenes", methods=['POST'])
def cargar_imagenes():
    files = request.files
    fl = files.listvalues()
    print(fl)

    for f  in fl:
        for f2 in f:
            rec = './temporales/' + f2.filename
            f2.save(rec)
    return "listo"

if __name__ == "__main__":
    try:
        os.mkdir("./temporales")
    except FileExistsError:
        pass

    app.run(host="0.0.0.0", port=8080, debug=True)
