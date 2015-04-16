import datetime,time,json,sys

def transfile(sourcefile, outputfile):
    dateformat = "%Y%m%d%H%M%S"
    sourcefile = open(sourcefile, "r")
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
    f = open(outputfile, "w")
    f.write(jsondata)
    f.close()

if __name__ == '__main__':  
    if (len(sys.argv) != 3):
        print('usage:transfile.py sourcefilename outputfilename')
        return
    transfile(sys.argv[1], sys.argv[2])