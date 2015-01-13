# -*- encoding: utf-8 -*-
import PointDefine_pb2
import datetime,string,time
import requests
import sys,os,json

kErrorCode = {395 : 'Input data is empty.', \
             396 : 'Decoding input data error.', \
             397 : 'Timo process has been broken down.', \
             398 : 'Clean Timo cache has failed.', \
             200 : 'Timo process is successed.', \
             399 : 'Content-Type is empty.', \
             500 : 'Program dumped.'}
#File format
kDataFormat = "%Y%m%d%H%M%S"
kFileColCount = 5
kFileDict = {'iAzimuth': 4, 
             'fGpsSpeed': 3, 
             'dLongitude': 0, 
             'dLatitude': 1, 
             'iGpsTime': 2
             }
#URL setting
kURL = 'http://172.26.183.48:5000/request'


def getallfilesfrompath(sourcepath, ext = None):
    allfiles = []
    needExtFilter = (ext != None)
    for root,paths,files in os.walk(sourcepath):
        for filespath in files:
            filepath = os.path.join(root, filespath)
            extension = os.path.splitext(filepath)[1][1:]
            if needExtFilter and extension in ext:
                allfiles.append(filepath)
            elif not needExtFilter:
                allfiles.append(filepath)
    return allfiles

def mkdir(path):
    path = path.strip()
    path = path.rstrip("/")
    
    isExists = os.path.exists(path)
    
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False
    
def test_request_multifile(sourcepath, outputpath):
    #get file list
    sourcepath = sourcepath.rstrip("/")
    outputpath = outputpath.rstrip("/")
    f = getallfilesfrompath(sourcepath, 'txt')
    costtime = float(0)
    for files in f:
        filename = os.path.basename(files)        
        splitname, shutfix = os.path.splitext(filename)
        pathname = os.path.split(os.path.dirname(files))
        pathname = pathname[len(pathname) - 1]
        filepath = outputpath + '/' + pathname
        mkdir(filepath)   
        sourcefile = open(files, "r")
        gpspointlist = PointDefine_pb2.pointlist()
        #read source file
        for oneline in sourcefile:
            listline = oneline.strip().split(',')
            if len(listline) != kFileColCount:
                continue
            gpspointlist.iAzimuth.append(string.atoi(listline[4]))
            gpspointlist.fGpsSpeed.append(string.atof(listline[3]))
            gpspointlist.dLongitude.append(string.atof(listline[0]))
            gpspointlist.dLatitude.append(string.atof(listline[1]))
            t = datetime.datetime.strptime(listline[2], kDataFormat)
            utcseconds = time.mktime(t.timetuple())
            gpspointlist.iGpsTime.append(int(utcseconds))
        sourcefile.close()
        tstart = time.time()
        point_str = gpspointlist.SerializeToString()
        
        headers = {'content-Type':'application/octet-stream'}
        result = requests.post(kURL, data=str(point_str), headers=headers)
        if result.status_code != 200:
            print (files, kErrorCode[result.status_code])
            continue    
        #process proto
        trafficinfoheader_proto = PointDefine_pb2.trafficinfoheader()
        trafficinfoheader_proto.ParseFromString(result.content)
        tend = time.time()
        costtime = costtime + float(tend - tstart)
        savefilepath = filepath  + '/' + splitname + '.txt'
        savefile = open(savefilepath, "w")
        for i in range(len(trafficinfoheader_proto.iTileID)):
            strsave = 'index:' + str(i) + '\n' + \
                        'tileid:' + str(trafficinfoheader_proto.iTileID[i]) + '\n' + \
                        'linkid:'+ str(trafficinfoheader_proto.iLinkID[i]) + '\n' + \
                        'dir:'+ str(trafficinfoheader_proto.iLinkDir[i]) + '\n' + \
                        'length:' + str(trafficinfoheader_proto.fLinkLength[i]) + '\n' + \
                        'AverageSpeed:' + str(trafficinfoheader_proto.fAverageSpeed[i]) + '\n' + \
                        'MaxSpeed:' + str(trafficinfoheader_proto.fMaxSpeed[i]) + '\n'
            savefile.write(strsave)
        savefile.close()
    print "cost time:%f" % costtime        

def test_json_multifile(sourcepath, outputpath):
    #get file list
    sourcepath = sourcepath.rstrip("/")
    outputpath = outputpath.rstrip("/")
    f = getallfilesfrompath(sourcepath, 'txt')
    costtime = float(0.0)
    gpscount = int(0)
    for files in f:
        filename = os.path.basename(files)        
        splitname, shutfix = os.path.splitext(filename)
        pathname = os.path.split(os.path.dirname(files))
        pathname = pathname[len(pathname) - 1]
        filepath = outputpath + '/' + pathname
        mkdir(filepath)   
        sourcefile = open(files, "r")
        jsonlist = []
        #read source file
        for oneline in sourcefile:
            listline = oneline.strip().split(',')
            if len(listline) != kFileColCount:
                continue
            gpscount = gpscount + 1
            t = datetime.datetime.strptime(listline[kFileDict['iGpsTime']], kDataFormat)
            utcseconds = time.mktime(t.timetuple())
            tel = {'iAzimuth':listline[kFileDict['iAzimuth']], \
                   'fGpsSpeed':listline[kFileDict['fGpsSpeed']], \
                   'dLongitude':listline[kFileDict['dLongitude']], \
                   'dLatitude':listline[kFileDict['dLatitude']], \
                   'iGpsTime':str(int(utcseconds))}
            jsonlist.append(tel)
        sourcefile.close()
        jsondata = json.dumps(jsonlist)
        tstart = time.time()

        headers = {'content-Type':'application/json'}
        result = requests.post(kURL, data=str(jsondata), headers=headers)
        if result.status_code != 200:
            print (files, kErrorCode[result.status_code])
            continue    
        #process json
        try:
            newdata = json.loads(result.content)
        except ValueError:
            print 'result is not json format.'
            continue
        tend = time.time()
        costtime = costtime + float(tend - tstart)
        savefilepath = filepath  + '/' + splitname + '.txt'
        savefile = open(savefilepath, "w")
        for i in range(len(newdata)):
            strsave = 'index:' + str(i) + '\n' + \
                        'tileid:' + str(newdata[i]['iTileID']) + '\n' + \
                        'linkid:'+ str(newdata[i]['iLinkID']) + '\n' + \
                        'dir:'+ str(newdata[i]['iLinkDir']) + '\n' + \
                        'length:' + str(newdata[i]['fLinkLength']) + '\n' + \
                        'AverageSpeed:' + str(newdata[i]['fAverageSpeed']) + '\n' + \
                        'MaxSpeed:' + str(newdata[i]['fMaxSpeed']) + '\n'
            savefile.write(strsave)
        savefile.close()
    print "gpscount:%d, cost time:%f" % (gpscount, costtime)  

def test_request_onefile(sourcefile):
    gpspointlist = PointDefine_pb2.pointlist()
    sourcefile = open(sourcefile, "r")
    for oneline in sourcefile:
        listline = oneline.strip().split(',')
        if len(listline) != kFileColCount:
            continue
        gpspointlist.iAzimuth.append(string.atoi(listline[4]))
        gpspointlist.fGpsSpeed.append(string.atof(listline[3]))
        gpspointlist.dLongitude.append(string.atof(listline[0]))
        gpspointlist.dLatitude.append(string.atof(listline[1]))
        t = datetime.datetime.strptime(listline[2], kDataFormat)
        utcseconds = time.mktime(t.timetuple())
        gpspointlist.iGpsTime.append(int(utcseconds))
    sourcefile.close()
    tstart = time.time()        
    point_str = gpspointlist.SerializeToString()
    
    headers = {'content-Type':'application/octet-stream'}
    result = requests.post(kURL, data=str(point_str), headers=headers)
    if result.status_code != 200:
        print (sourcefile, kErrorCode[result.status_code])
        return        
    #process proto
    trafficinfoheader_proto = PointDefine_pb2.trafficinfoheader()
    trafficinfoheader_proto.ParseFromString(result.content)
    for i in range(len(trafficinfoheader_proto.iTileID)):
        print trafficinfoheader_proto.iTileID[i], trafficinfoheader_proto.iLinkID[i], trafficinfoheader_proto.iLinkDir[i]
    print "cost time:%s" % (time.time() - tstart)
    
if __name__ == '__main__':  
    if (len(sys.argv) == 2):
        test_request_onefile(sys.argv[1])
    elif (len(sys.argv) == 4):
        if sys.argv[3] == 'stream':
            test_request_multifile(sys.argv[1], sys.argv[2])
        elif sys.argv[3] == 'json':
            test_json_multifile(sys.argv[1], sys.argv[2])
    else:
        print('usage:filename.py sourcepath outpath type or filename.py sourcefile')
        
        
        