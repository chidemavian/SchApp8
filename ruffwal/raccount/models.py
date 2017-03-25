from django.db import models
from datetime import datetime, timedelta

# Create your models here.
class useracc(models.Model):
    username = models.CharField("Username",max_length = 160,primary_key= True,null = False )
    password = models.CharField("Password",max_length = 50,null = False )
    subtimestamp = models.DateTimeField(auto_now_add=True, blank=True)


    def __unicode__(self):
        return  u'%s %s %s' % (self.username,self.password,self.subtimestamp)
    class Meta:
        ordering =['-subtimestamp',]
        verbose_name_plural = "User Account"