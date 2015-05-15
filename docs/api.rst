.. _api:

API
===

POST /timo
----------

The single major api of this application, used to post a couple of gps points.

Post some gps points of one trace, then the response is the matched links.

========================  ============    =============
Content-Type              input format    output format
========================  ============    =============
application/octet-stream  protobuf        protobuf
application/json          json            json
========================  ============    =============


GET /health_check
-----------------
::

    $ curl http://localhost:5000/health_check
    {
  	"config": {
   	  "TIMO_LIB_DATA_PATH": "/mnt/data/forcpp.dat",
    	  "TIMO_LIB_MATCH_ANGLE": 40,
    	  "TIMO_LIB_MATCH_RADIUS": 40,
    	  "TIMO_LIB_MAX_TIMEGAP": 120,
    	  "TIMO_LIB_MIN_TIMEGAP": 4,
    	  "TIMO_LIB_PATH": "/usr/local/lib/libtimo.so"
  	},
  	"flask": "0.10.1",
  	"version": "1.0.0"
    }


GET /describe
-------------
::

    $ curl http://localhost:5000/health_check
    {
  	"config": {
   	  "TIMO_LIB_DATA_PATH": "/mnt/data/forcpp.dat",
    	  "TIMO_LIB_MATCH_ANGLE": 40,
    	  "TIMO_LIB_MATCH_RADIUS": 40,
    	  "TIMO_LIB_MAX_TIMEGAP": 120,
    	  "TIMO_LIB_MIN_TIMEGAP": 4,
    	  "TIMO_LIB_PATH": "/usr/local/lib/libtimo.so"
  	},
  	"flask": "0.10.1",
  	"version": "1.0.0"
    }
