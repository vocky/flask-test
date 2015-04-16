# -*- encoding: utf-8 -*-
# We'll render HTML templates and access data sent by POST
# using the request object from flask
from flask import Flask, request, abort, make_response, current_app
import timolib
import os
# Initialize the Flask application

def jsonreq():
    # Get the JSON data sent from the form
    #     jsondata = request.form['jsondata']
    #     #data = timolib.decodingjson(jsondata)
    #     data = jsondata
    #     return render_template('request.html', data=data, jsondata=jsondata)
    timolibrary = current_app.timolibrary
    content_type = request.headers['Content-Type']
    if content_type == 'application/octet-stream': 
        return timolibrary.decodingdata(request.get_data())
    elif content_type == 'application/json':
        return timolibrary.decoding2json(request.get_data())
    elif content_type == 'application/xml':
        return timolibrary.decoding2xml(request.get_data())
    else:
        abort(make_response("Content-Type Error", 399))
            
def create_app(config=None):
    """Create timorest application
    Config tries the following:
    1. 'config' parameter
    2. 'TIMO_APP_SETTINGS' from the environment variable
    3. 'settings.cfg' file in current path
    
    All config prefixed with 'TIMO_' can be overridden by direct envvar
    """
    app = Flask(__name__)
    
    app.config.from_object('timorest.default_settings')
    
    if config:
        if isinstance(config, dict):
            app.config.update(config)
        else:
            app.config.from_pyfile(config)
    else:
        app.config.from_envvar('TIMO_APP_SETTINGS', silent=True)
        
    env_override = dict((k, v) for k, v in os.environ.items() \
                        if k.startswith('TIMO_'))
    app.config.update(env_override)
    
    timolibrary = timolib.timolibrary(app.config)

# This route will show a form to submit some JSON data
# This route will accept a request containing JSON
# Then we'll convert that data into Python a structure
# and print it.
# Because we used a standard HTML form post to send the
# data, we need to get the JSON from request.form
# If on other hand the information was sent from an app,
# or even a python urllib2.Request we would need to use
# request.data to get the JSON string
    app.timolibrary = timolibrary
    app.add_url_rule(app.config['TIMO_REQUEST_URL'], 'jsonreq', jsonreq, methods=['POST',])
    return app