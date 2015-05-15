.. _config:

Configuration
=============
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
