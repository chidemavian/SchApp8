import datetime

def gettime():
    tday = datetime.datetime.now()
    return 'Printed Date :' + tday.strftime('%d-%b,%Y:%H:%M')
