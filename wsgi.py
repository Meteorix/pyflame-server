from gevent.monkey import patch_all; patch_all()
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template, Response, send_file
import subprocess as sb
import time
import os
import io


app = Flask(__name__)
UPLOAD_DIR = "./uploads"


@app.route("/")
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        fs = request.files['file']
        filepath = os.path.join(UPLOAD_DIR, "%s.%s" % (fs.filename, time.time()))
        app.logger.warn("saving %s to %s" % (fs, filepath))
        fs.save(filepath)

        svgpath = filepath + ".svg"
        out = txt_2_svg(filepath, svgpath)
        app.logger.warn("txt_2_svg %s" % out)

        return request.url_root + "svg/" + os.path.basename(svgpath) + "\n"
    else:
        return render_template("upload.html")


@app.route("/svg")
def svg_list():
    data = []
    fs = os.listdir(UPLOAD_DIR)
    for f in fs:
        if not f.endswith(".svg"):
            continue
        name = os.path.basename(f)
        url = request.url_root + "svg/" + name
        data.append({"url": url, "name": name})
    return render_template("list.html", data=data)


@app.route("/svg/<filename>")
def svg(filename):
    filepath = os.path.join(UPLOAD_DIR, filename)
    f = open(filepath)
    r = Response(f.read(), mimetype="image/svg+xml")
    return r


@app.route("/pyflame")
def pyflame():
    return send_file("./pyflame")


def txt_2_svg(txt, svg):
    cmd = "./flamegraph.pl %s > %s" % (txt, svg)
    out = sb.check_output(cmd, shell=True)
    return out



if __name__ == "__main__":
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    host, port = "0.0.0.0", 5000
    print("gevent server staring on http://%s:%s" % (host, port))
    WSGIServer((host, int(port)), app).serve_forever()

