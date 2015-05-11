# -*- encoding: utf-8 -*-
import PointDefine_pb2
import ctypes
import json
from flask import abort, make_response
import dicttoxml
import string


class LibConfig(ctypes.Structure):
    _fields_=[('kMatchRadius', ctypes.c_int),
              ('kMatchAngle', ctypes.c_int),
              ('kMinTimeInterval', ctypes.c_int),
              ('kMaxTimeInterval', ctypes.c_int),
              ('libpath', ctypes.c_char * 256)]
    def getdict(self):
        return dict((f, getattr(self, f)) for f, _ in self._fields_)


class CarGpsData(ctypes.Structure):
    _fields_=[('iGpsTime', ctypes.c_int),
              ('iAzimuth', ctypes.c_int),
              ('fGpsSpeed', ctypes.c_float),
              ('dLongitude', ctypes.c_double),
              ('dLatitude', ctypes.c_double)]
    def getdict(self):
        return dict((f, getattr(self, f)) for f, _ in self._fields_)


# gps list header
class CarGpsHeader(ctypes.Structure):
    _fields_=[('iGPSCount', ctypes.c_int),
               ('pstGPSData', ctypes.POINTER(CarGpsData))]


class TrafficInfo(ctypes.Structure):
    _fields_=[('iTileID', ctypes.c_int),
              ('iLinkID', ctypes.c_int),
              ('iLinkDir', ctypes.c_int),
              ('iLinkDegree', ctypes.c_int),
              ('iTime', ctypes.c_int),
              ('IsConnected', ctypes.c_int),
              ('fLinkLength', ctypes.c_float),
              ('fPathLength', ctypes.c_float),
              ('fAverageSpeed', ctypes.c_float),
              ('fMaxSpeed', ctypes.c_float)]
    def getdict(self):
        return dict((f, getattr(self, f)) for f, _ in self._fields_)


# Traffic information header
class TrafficInfoHeader(ctypes.Structure):
    _fields_=[('iTrafficInfoCount', ctypes.c_int),
              ('pstTrafficInfoData', ctypes.POINTER(TrafficInfo))]
        

class TimoLibrary(object):
    def __init__(self, config):
        timo_library = ctypes.cdll.LoadLibrary(config['TIMO_LIB_PATH'])
        if timo_library == None:
            raise Exception('TIMO_LIB_PATH library is not found.') 
        # init api
        self.inittimo = timo_library.InitTimo3
        self.inittimo.restype = ctypes.c_void_p
        self.inittimo.argtypes = [ctypes.POINTER(LibConfig)]
        self.ProcessTimo = timo_library.ProcessTimo
        self.ProcessTimo.argtypes = [ctypes.c_void_p, ctypes.POINTER(CarGpsHeader), ctypes.POINTER(TrafficInfoHeader)]
        self.ProcessTimo.restype = None
        self.CleanTimoCache = timo_library.CleanTimoCache
        self.CleanTimoCache.argtypes = [ctypes.c_void_p, ctypes.POINTER(TrafficInfoHeader)]
        self.CleanTimoCache.restype = None
        self.CloseTimo = timo_library.CloseTimo
        self.CloseTimo.argtypes = [ctypes.c_void_p]
        self.CloseTimo.restype = None
        self._timolib = ctypes.c_void_p()
        # initialize config
        libconfig = LibConfig()
        libconfig.kMatchRadius = config['TIMO_LIB_MATCH_RADIUS']
        libconfig.kMatchAngle = config['TIMO_LIB_MATCH_ANGLE']
        libconfig.kMinTimeInterval = config['TIMO_LIB_MIN_TIMEGAP']
        libconfig.kMaxTimeInterval = config['TIMO_LIB_MAX_TIMEGAP']
        libconfig.libpath = config['TIMO_LIB_DATA_PATH']
        self._timolib = self.inittimo(ctypes.byref(libconfig))
        if self._timolib == None:
            raise Exception('initial failed.')
    
    def __enter__(self):
        return self
    
    def __exit__(self):
        self.CloseTimo(ctypes.c_void_p(self._timolib))  
        
    def close(self):
        self.CloseTimo(ctypes.c_void_p(self._timolib))    
    
    def gettrafficinfolist(self, proto):
        inputheader = CarGpsHeader()
        pointlist_proto = PointDefine_pb2.pointlist()
        try:
            pointlist_proto.ParseFromString(proto)
        except:
            abort(make_response("Parse Error", 400))
        #initialize gps header
        inputheader.iGPSCount = len(pointlist_proto.iGpsTime)
        if inputheader.iGPSCount == 0:
            abort(make_response("Input Error", 400))
        inputheader.pstGPSData = (inputheader.iGPSCount * CarGpsData)()
        for i in range(inputheader.iGPSCount):
            inputheader.pstGPSData[i].iGpsTime = pointlist_proto.iGpsTime[i]
            inputheader.pstGPSData[i].iAzimuth = pointlist_proto.iAzimuth[i]
            inputheader.pstGPSData[i].fGpsSpeed = pointlist_proto.fGpsSpeed[i]
            inputheader.pstGPSData[i].dLongitude = pointlist_proto.dLongitude[i]
            inputheader.pstGPSData[i].dLatitude = pointlist_proto.dLatitude[i]
            
        trafficinfolist = TrafficInfoHeader()
        trafficinfolist.iTrafficInfoCount = 0
        trafficinfolist.pstTrafficInfoData = None
        #process
        try:
            if self._timolib is not None:
                self.ProcessTimo(ctypes.c_void_p(self._timolib), ctypes.byref(inputheader), ctypes.byref(trafficinfolist))
        except:
            abort(make_response("Process Error", 500))
        return trafficinfolist
        
    def decodingdata(self, proto):
        trafficinfolist = self.gettrafficinfolist(proto)
        #encoding to protobuff
        trafficinfoheader_proto = PointDefine_pb2.trafficinfoheader()
        for i in range(trafficinfolist.iTrafficInfoCount):
            trafficinfoheader_proto.iTileID.append(trafficinfolist.pstTrafficInfoData[i].iTileID)
            trafficinfoheader_proto.iLinkID.append(trafficinfolist.pstTrafficInfoData[i].iLinkID)
            trafficinfoheader_proto.iLinkDir.append(trafficinfolist.pstTrafficInfoData[i].iLinkDir)
            trafficinfoheader_proto.iLinkDegree.append(trafficinfolist.pstTrafficInfoData[i].iLinkDegree)
            trafficinfoheader_proto.iTime.append(trafficinfolist.pstTrafficInfoData[i].iTime)
            trafficinfoheader_proto.IsConnected.append(trafficinfolist.pstTrafficInfoData[i].IsConnected)
            trafficinfoheader_proto.fLinkLength.append(trafficinfolist.pstTrafficInfoData[i].fLinkLength)
            trafficinfoheader_proto.fPathLength.append(trafficinfolist.pstTrafficInfoData[i].fPathLength)
            trafficinfoheader_proto.fAverageSpeed.append(trafficinfolist.pstTrafficInfoData[i].fAverageSpeed)
            trafficinfoheader_proto.fMaxSpeed.append(trafficinfolist.pstTrafficInfoData[i].fMaxSpeed)
        #clean cache
        try:
            if self._timolib is not None:
                self.CleanTimoCache(ctypes.c_void_p(self._timolib), ctypes.byref(trafficinfolist))
        except:
            abort(make_response("Clean Error", 500))
        #transform to buff
        outputstr = trafficinfoheader_proto.SerializeToString()
        return outputstr
    
    def decoding2json(self, proto):
        try:
            newdata = json.loads(proto)
        except:
            abort(make_response("Decoding  Error", 400))
            
        inputheader = CarGpsHeader()
        #initialize gps header
        inputheader.iGPSCount = len(newdata)
        if inputheader.iGPSCount == 0:
            abort(make_response("Input Error", 400))
        inputheader.pstGPSData = (inputheader.iGPSCount * CarGpsData)()
        try:
            for i in range(inputheader.iGPSCount):
                inputheader.pstGPSData[i].iGpsTime = string.atoi(newdata[i]['iGpsTime'])
                inputheader.pstGPSData[i].iAzimuth = string.atoi(newdata[i]['iAzimuth'])
                inputheader.pstGPSData[i].fGpsSpeed = string.atof(newdata[i]['fGpsSpeed'])
                inputheader.pstGPSData[i].dLongitude = string.atof(newdata[i]['dLongitude'])
                inputheader.pstGPSData[i].dLatitude = string.atof(newdata[i]['dLatitude'])
        except:
            abort(make_response("Input Error", 500))
                                
        trafficinfolist = TrafficInfoHeader()
        trafficinfolist.iTrafficInfoCount = 0
        trafficinfolist.pstTrafficInfoData = None
        #process
        try:
            if self._timolib is not None:
                self.ProcessTimo(ctypes.c_void_p(self._timolib), ctypes.byref(inputheader), ctypes.byref(trafficinfolist))
        except:
            abort(make_response("Process Error", 500))
        #encoding to json
        jsonlist = []
        for i in range(trafficinfolist.iTrafficInfoCount):
            jsonlist.append(trafficinfolist.pstTrafficInfoData[i].getdict())           
        #clean cache
        try:
            if self._timolib is not None:
                self.CleanTimoCache(ctypes.c_void_p(self._timolib), ctypes.byref(trafficinfolist))
        except:
            abort(make_response("Clean Error", 500))
        return json.dumps(jsonlist)
    
    def decoding2xml(self, proto):
        trafficinfolist = self.gettrafficinfolist(proto)
        jsonlist = []
        for i in range(trafficinfolist.iTrafficInfoCount):
            jsonlist.append(trafficinfolist.pstTrafficInfoData[i].getdict())        
        #clean cache
        try:
            if self._timolib is not None:
                self.CleanTimoCache(ctypes.c_void_p(self._timolib), ctypes.byref(trafficinfolist))
        except:
            abort(make_response("Clean Error", 500))
        xml = dicttoxml.dicttoxml(jsonlist)
        return xml
    
    
    