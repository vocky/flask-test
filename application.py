#! /usr/bin/env python

"""the application that runs timorest"""

from timorest import create_app

app = application = create_app()

if __name__ == '__main__':
    #app.debug = True 
    app.run(host="0.0.0.0")
