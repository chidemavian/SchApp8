import datetime
from datetime import  date
def getmonth(startdate,enddate):
    transdate = startdate
    d = 1
    for p in range(1,12):
        endyear = enddate.year
        endmonth = enddate.month
        #*********************************
        month = transdate.month
        year = transdate.year
        if month == endmonth and year == endyear:
            break
            #********************************************
        month += 1
        if month == 13:
            month = 1
            year += 1
        else:
            year = year
        transdate = date(year,month,1)
        d +=1
    return d
