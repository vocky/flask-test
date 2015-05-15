.. _quickstart:

Quickstart
==========
It assumes that:
+ You already have Timorest installed.
+ Flask/protobuf/dicttoxml have installed.

A Minimal Appllication
----------------------
We've provided a ready-to-use application.py wsgi portal.
to debug::

    $ python application.py

json Request
------------
::

    $ curl -X POST -H "Content-Type:application/json" -d '[{"dLongitude": "140.206185961", "iGpsTime": "1399117967", "dLatitude": "35.6821634769", "fGpsSpeed": "127", "iAzimuth": "267"},{"dLongitude": "140.203765377", "iGpsTime": "1399117974", "dLatitude": "35.6821178432", "fGpsSpeed": "122", "iAzimuth": "271"}]' http://localhost:5000/timo

::

    [{"iLinkID": 411, "iTime": 1399117974, "fLinkLength": 2004.0, "fAverageSpeed": 119.53248596191406, "iLinkDegree": 0, "fMaxSpeed": 119.53248596191406, "IsConnected": 1, "iTileID": -298116813, "iLinkDir": 0, "fPathLength": 332.03466796875}]

health_check
------------
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

Normal response codes
---------------------
+ **200 OK**
+ **400 Bad Request** - e.g. invalid request data/format/headers.
+ **500 process dumped**
