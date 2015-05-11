Timorest - Timo library service
===============================
+ This project depends on timo project.
+ You must ensure the shared library of TIMO_LIB_PATH is existed. You can refer to project Timo.

Installation
------------
+ Installing Timorest requires Python 2.7, with setuptools pre-installed.
+ Simply run ``sudo python setup.py install`` will do the trick.

Settings
--------
Config tries the following:

1. 'config' parameter.
2. 'TIMO_APP_SETTINGS' from the environment variable.
3. 'settings.cfg' file in current path.


All config prefixed with ``TIMO_`` can be overridden by direct envvar.

=====================  =========== 
config parameters      about
=====================  =========== 
TIMO_LIB_PATH          Abs path of the timo c library. Default is in /usr/local/lib/.
TIMO_LIB_DATA_PATH     Abs path of timo source data file.
TIMO_LIB_MIN_TIMEGAP   The min time gap between two gps points.
TIMO_LIB_MAX_TIMEGAP   The max time gap between two gps points.
TIMO_LIB_MATCH_RADIUS  Match radius.
TIMO_LIB_MATCH_ANGLE   Match angle.
=====================  =========== 

Running & Deploying
-------------------
We've provided a ready-to-use application.py wsgi portal.
to debug:

    ./application.py
    
API
------------
``POST /timo``

The single major api of this application, used to post a couple of gps points.

Post some gps points of one trace, then the response is the matched links.

========================  ============    =============
Content-Type              input format    output format
========================  ============    =============
application/octet-stream  protobuf        protobuf
application/json          json            json
========================  ============    =============

Example
-------
`Post:`

```curl -X POST -H "Content-Type:application/json" -d '[{"dLongitude": "140.206185961", "iGpsTime": "1399117967", "dLatitude": "35.6821634769", "fGpsSpeed": "127", "iAzimuth": "267"},{"dLongitude": "140.203765377", "iGpsTime": "1399117974", "dLatitude": "35.6821178432", "fGpsSpeed": "122", "iAzimuth": "271"}]' http://localhost:5000/timo```

`Response:`

```[{"iLinkID": 411, "iTime": 1399117974, "fLinkLength": 2004.0, "fAverageSpeed": 119.53248596191406, "iLinkDegree": 0, "fMaxSpeed": 119.53248596191406, "IsConnected": 1, "iTileID": -298116813, "iLinkDir": 0, "fPathLength": 332.03466796875}]```

`Normal response codes:`

+ `200 OK`
+ `400 Bad Request` - e.g. invalid request data/format/headers.
+ `500 process dumped`
