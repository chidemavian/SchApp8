
from myproject.academics.models import *
from myproject.student.models import *


def classavg(self):
    a = SubjectScore.objects.filter(subject=self.subject, term=self.term,
        session=self.session, klass=self.klass,
        arm=self.arm).aggregate(Avg('term_score'))
    kk = a['term_score__avg']
    return kk

def juniorgrade(score):
    if (score >=70) and (score <= 100):
        grade = 'A'
        remark = 'Excellent'
    elif (score >=50) and (score <= 69.9):
        grade = 'C'
        remark = 'Credit'
    elif (score >=40) and (score <= 49.9):
        grade = 'P'
        remark = 'Pass'
    elif (score >=0) and (score <= 39.9):
        grade = 'F'
        remark = 'Poor'
    else:
        grade = ''
        remark = ''
    return {'remark':remark,'grade':grade}

def seniorgrade(score):
    if (score >=75.0) and (score <= 100):
        grade = 'A1'
        remark = 'Excellent'
    elif (score >=70.0) and (score <= 74.9):
        grade = 'B2'
        remark = 'Very Good'
    elif (score >=65.0) and (score <= 69.9):
        grade = 'B3'
        remark = 'Good'
    elif (score >=60.0) and (score <= 64.9):
        grade = 'C4'
        remark = 'Credit'
    elif (score >=55.0) and (score <= 59.9):
        grade = 'C5'
        remark = 'Credit'
    elif (score >=50.0) and (score <= 54.9):
        grade = 'C6'
        remark = 'Credit'
    elif (score >=45.0) and (score <= 49.9):
        grade = 'D7'
        remark = 'Pass'
    elif (score >=40.0) and (score <= 44.9):
        grade = 'E8'
        remark = 'Pass'
    elif (score >=0.0) and (score <= 39.9):
        grade = 'F9'
        remark = 'Fail'
    else:
        grade =''
        remark = 'Good'
    return {'remark':remark,'grade':grade}

def prygrade(score):
    if (score >=85) and (score <= 100):
        grade = 'A'
        remark = 'Excellent'
    elif (score >=70) and (score <= 84.9):
        grade = 'B'
        remark = 'Very Good'
    elif (score >=55) and (score <= 69.9):
        grade = 'C'
        remark = 'Good'
    elif (score >=40) and (score <= 54.9):
        grade = 'D'
        remark = 'Fair'
    elif (score >=0) and (score <= 39.9):
        grade = 'F'
        remark = 'Fail'
    else:
        grade ='F'
        remark ='Fail'
    return {'remark':remark,'grade':grade}




