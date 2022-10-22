#!/usr/bin/python3
'''
    flask with general routes
    routes:
        /status:    display "status":"OK"
'''
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """return status ok json formatted"""
    return jsonify({"status": "OK"})
