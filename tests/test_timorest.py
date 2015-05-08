import unittest
import os,string
import json
from timorest import default_settings as settings
from timorest import PointDefine_pb2
from timorest import create_app

kErrorCode = {395 : 'Input data is empty.', \
             396 : 'Decoding input data error.', \
             397 : 'Timo process has been broken down.', \
             398 : 'Clean Timo cache has failed.', \
             200 : 'Timo process is successed.', \
             399 : 'Content-Type is empty.', \
             500 : 'Program dumped.'}


class TimoTestCase(unittest.TestCase):
    def setUp(self):
        self.assertTrue(os.path.isfile(settings.TIMO_LIB_PATH))
        self.app = create_app(config = {'TIMO_LIB_DATA_PATH': 'forcpp.dat'})
        self.assertTrue(self.app)
        self.assertEqual(self.app.config['TIMO_LIB_MIN_TIMEGAP'], settings.TIMO_LIB_MIN_TIMEGAP)
        self.assertEqual(self.app.config['TIMO_LIB_MAX_TIMEGAP'], settings.TIMO_LIB_MAX_TIMEGAP)
        self.assertEqual(self.app.config['TIMO_LIB_MATCH_RADIUS'], settings.TIMO_LIB_MATCH_RADIUS)
        self.assertEqual(self.app.config['TIMO_LIB_MATCH_ANGLE'], settings.TIMO_LIB_MATCH_ANGLE)
        self.app.testing = True
        self.client = self.app.test_client()
        # read result data
        self.assertTrue(os.path.isfile('output.json'))
        file_object = open('output.json', 'r')
        try:
            jsondata = file_object.read()
        finally:
            file_object.close()
        self.resultdata = json.loads(jsondata)
    
    def tearDown(self):
        self.app.timolibrary.close()
        
    def test_json_post(self):
        # read json file
        self.assertTrue(os.path.isfile('input.json'))
        file_object = open('input.json', 'r')
        try:
            jsondata = file_object.read()
        finally:
            file_object.close()
        headers = [('Content-Type', 'application/json')]
        response = self.client.post('/timo', \
                                    data=str(jsondata), headers=headers)
        self.assertEqual(response.status_code, 200)
        outputjson = json.loads(response.data)
        self.assertEqual(len(outputjson), len(self.resultdata))
        for i in range(len(outputjson)):
            self.assertEqual(outputjson[i]['iTileID'], self.resultdata[i]['iTileID'])
            self.assertEqual(outputjson[i]['iLinkID'], self.resultdata[i]['iLinkID'])
    
    def test_oct_post(self):
        # read json file
        self.assertTrue(os.path.isfile('input.json'))
        file_object = open('input.json', 'r')
        try:
            strdata = file_object.read()
        finally:
            file_object.close()
        # json transfer to protobuf
        gpspointlist = PointDefine_pb2.pointlist()
        jsondata = json.loads(strdata)
        for i in range(len(jsondata)):
            gpspointlist.iAzimuth.append(string.atoi(jsondata[i]['iAzimuth']))
            gpspointlist.fGpsSpeed.append(string.atof(jsondata[i]['fGpsSpeed']))
            gpspointlist.dLongitude.append(string.atof(jsondata[i]['dLongitude']))
            gpspointlist.dLatitude.append(string.atof(jsondata[i]['dLatitude']))
            gpspointlist.iGpsTime.append(string.atoi(jsondata[i]['iGpsTime']))
        headers = [('Content-Type', 'application/octet-stream')]
        point_str = gpspointlist.SerializeToString()
        response = self.client.post('/timo', \
                                    data=str(point_str), headers=headers)
        self.assertEqual(response.status_code, 200)
        #process proto
        trafficinfoheader_proto = PointDefine_pb2.trafficinfoheader()
        try:
            trafficinfoheader_proto.ParseFromString(response.data)
        except:
            raise Exception("Parse protobuff failed.")

        for i in range(len(trafficinfoheader_proto.iTileID)):
            self.assertEqual(trafficinfoheader_proto.iTileID[i], self.resultdata[i]['iTileID'])
            self.assertEqual(trafficinfoheader_proto.iLinkID[i], self.resultdata[i]['iLinkID'])
    
    def test_xml_post(self):
        # read json file
        self.assertTrue(os.path.isfile('input.json'))
        file_object = open('input.json', 'r')
        try:
            strdata = file_object.read()
        finally:
            file_object.close()
        # json transfer to xml
        gpspointlist = PointDefine_pb2.pointlist()
        jsondata = json.loads(strdata)
        for i in range(len(jsondata)):
            gpspointlist.iAzimuth.append(string.atoi(jsondata[i]['iAzimuth']))
            gpspointlist.fGpsSpeed.append(string.atof(jsondata[i]['fGpsSpeed']))
            gpspointlist.dLongitude.append(string.atof(jsondata[i]['dLongitude']))
            gpspointlist.dLatitude.append(string.atof(jsondata[i]['dLatitude']))
            gpspointlist.iGpsTime.append(string.atoi(jsondata[i]['iGpsTime']))
        headers = [('Content-Type', 'application/xml')]
        point_str = gpspointlist.SerializeToString()
        response = self.client.post('/timo', \
                                    data=str(point_str), headers=headers)
        self.assertEqual(response.status_code, 200)
        
    def test_other_post(self):
        headers = [('Content-Type', 'application/txt')]
        response = self.client.post('/timo', \
                                    data='str', headers=headers)
        self.assertEqual(response.status_code, 399)
        
    def test_errorjson_post(self):
        headers = [('Content-Type', 'application/json')]
        response = self.client.post('timo', \
                                    data='str', headers=headers)
        self.assertEqual(response.status_code, 396)
        
    def test_init(self):
        current_dir = os.getcwd()
        cfg = os.path.join(current_dir, 'settings.cfg')
        app = create_app(cfg)
        self.assertEqual(app.config['TIMO_LIB_MAX_TIMEGAP'], 100)
        self.assertEqual(app.config['TIMO_LIB_MATCH_RADIUS'], 30)
        app.timolibrary.close()

if __name__ == '__main__':
    unittest.main()