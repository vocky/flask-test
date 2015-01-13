# -*- encoding: utf-8 -*-
import timo
import unittest
import PointDefine_pb2
import datetime,string,time,json

kErrorCode = {395 : 'Input data is empty.', \
             396 : 'Decoding input data error.', \
             397 : 'Timo process has been broken down.', \
             398 : 'Clean Timo cache has failed.', \
             200 : 'Timo process is successed.', \
             399 : 'Content-Type is empty.', \
             500 : 'Program dumped.'}

class TimoTestCase(unittest.TestCase):
    def setUp(self):
        self.app = timo.app.test_client()

    def test_request_post(self):
        gpspointlist = PointDefine_pb2.pointlist()
        dateformat = "%Y%m%d%H%M%S"
        sourcefile = open('120.txt', "r")
        for oneline in sourcefile:
            listline = oneline.strip().split(',')
            if len(listline) != 5:
                continue
            gpspointlist.iAzimuth.append(string.atoi(listline[4]))
            gpspointlist.fGpsSpeed.append(string.atof(listline[3]))
            gpspointlist.dLongitude.append(string.atof(listline[0]))
            gpspointlist.dLatitude.append(string.atof(listline[1]))
            t = datetime.datetime.strptime(listline[2], dateformat)
            utcseconds = time.mktime(t.timetuple())
            gpspointlist.iGpsTime.append(int(utcseconds))
        sourcefile.close()
                
        point_str = gpspointlist.SerializeToString()
        headers = {'content-Type':'application/octet-stream'}
        result = self.app.post('/request', data=str(point_str), headers=headers, follow_redirects=True)
        if result.status_code != 200:
            timo.timolibrary.close()
            print kErrorCode[result.status_code]
            return
        #process proto
        trafficinfoheader_proto = PointDefine_pb2.trafficinfoheader()
        try:
            trafficinfoheader_proto.ParseFromString(result.data)
        except:
            print "Parse protobuff failed."
        for i in range(len(trafficinfoheader_proto.iTileID)):
            print trafficinfoheader_proto.iTileID[i], trafficinfoheader_proto.iLinkID[i], trafficinfoheader_proto.iLinkDir[i]
            
    def test_json_post(self):
        dateformat = "%Y%m%d%H%M%S"
        sourcefile = open('120.txt', "r")
        jsonlist = []
        for oneline in sourcefile:
            listline = oneline.strip().split(',')
            if len(listline) != 5:
                continue
            t = datetime.datetime.strptime(listline[2], dateformat)
            utcseconds = time.mktime(t.timetuple())
            tel = {'iAzimuth':listline[4], 'fGpsSpeed':listline[3], 'dLongitude':listline[0], \
                        'dLatitude':listline[1], 'iGpsTime':str(int(utcseconds))}
            jsonlist.append(tel)
        sourcefile.close()
        
        jsondata = json.dumps(jsonlist)
        print 'test json output:'
        headers = {'content-Type':'application/json'}
        result = self.app.post('/request', data=str(jsondata), headers=headers, follow_redirects=True)
        if result.status_code != 200:
            timo.timolibrary.close()
            print kErrorCode[result.status_code]
            return
        
        try:
            newdata = json.loads(result.data)
        except ValueError:
            print 'result is not json format.'
        for i in range(len(newdata)):
            print newdata[i]['iTileID']
            print newdata[i]['iLinkID']
            
    def test_xml_post(self):
        gpspointlist = PointDefine_pb2.pointlist()
        dateformat = "%Y%m%d%H%M%S"
        sourcefile = open('120.txt', "r")
        for oneline in sourcefile:
            listline = oneline.strip().split(',')
            if len(listline) != 5:
                continue
            gpspointlist.iAzimuth.append(string.atoi(listline[4]))
            gpspointlist.fGpsSpeed.append(string.atof(listline[3]))
            gpspointlist.dLongitude.append(string.atof(listline[0]))
            gpspointlist.dLatitude.append(string.atof(listline[1]))
            t = datetime.datetime.strptime(listline[2], dateformat)
            utcseconds = time.mktime(t.timetuple())
            gpspointlist.iGpsTime.append(int(utcseconds))
        sourcefile.close()
        
        point_str = gpspointlist.SerializeToString()
        print 'test xml output:'
        headers = {'content-Type':'application/xml'}
        result = self.app.post('/request', data=str(point_str), headers=headers, follow_redirects=True)
        if result.status_code != 200:
            timo.timolibrary.close()
            print kErrorCode[result.status_code]
            return
        print result.data
        f = open("output.xml", "w")
        f.write(result.data)
        f.close()
if __name__ == '__main__':
    unittest.main()
    timo.timolibrary.close()
    
    
