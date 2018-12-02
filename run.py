# -*- coding:utf-8 -*-

from backend import create_app, socketio
from backend.config.LocalConfig import local

from flask import request, jsonify, render_template
from backend.models import *
from backend.common import *
from flask_socketio import emit

app = create_app(local)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10002, debug=True)
    # socketio.run(app, host="0.0.0.0", port= 10002)