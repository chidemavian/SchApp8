from django.db import models


class psetup(models.Model):
    klass = models.CharField('Class', max_length= 130)
    subject = models.CharField("Subject",max_length= 130)
    term = models.CharField("Term", max_length= 130)
    topic = models.CharField("Topic", max_length= 2000)
    num = models.CharField('session',max_length=15)
    count = models.CharField('session',max_length=15)
    session = models.CharField('session',max_length=15)

    def __unicode__(self):
        return self.topic


class psetsub(models.Model):
    klass = models.CharField('Class', max_length= 130,default = 'N/A')
    subject = models.CharField("Subject",max_length= 130,default = 'N/A')
    term = models.CharField("Term", max_length= 130,default = 'N/A')
    topic = models.ForeignKey(psetup, related_name = "Topic")
    #topic = models.CharField("Topic", max_length= 2000,default = 'N/A')
    session = models.CharField('session',max_length=15,default = 'N/A')
    subtopic = models.CharField("sub-topic", max_length= 2000,default = 'N/A')
    objectives = models.CharField("Topic", max_length= 2000, blank = True)
#    resource = models.CharField("Topic", max_length= 2000)
#    studentactivity = models.CharField("Topic", max_length= 2000)
#    teachersactivity = models.CharField("Topic", max_length= 2000)

    def __unicode__(self):
        return u'topic :%s,subtopic: %s' %(self.topic , self.subtopic)


class Psetweek(models.Model):
    lessonperweek = models.CharField("Lesson Per Week", max_length= 20)
    klass = models.CharField('Class', max_length= 130)
    subject = models.CharField("Subject",max_length= 130)
    teacherid = models.CharField("Topic", max_length= 2000)




class User(models.Model):
    username = models.CharField('Username',max_length = 40)
    klass = models.CharField('Class',max_length = 20)
    subject = models.CharField('Subject',max_length = 50)


