from django.db import models
from myproject.ruffwal.rsetup.models import tblaccount
# Create your models here.
class tblbudget(models.Model):
    acccode = models.ForeignKey(tblaccount)
    startmonth = models.DateField('Start Year')
    endmonth = models.DateField('End Year')
    userid = models.CharField("User Id",max_length = 150,null = False )
    acctype = models.CharField("Account Type",max_length = 150,default='')
    amount = models.DecimalField('Amount',max_digits = 20 , decimal_places = 2, null = True )
    refcode = models.CharField("Ref. Code",max_length = 550,default='')
    def __unicode__(self):
        return  u'%s %s %s %s' % (self.acccode.acccode,self.startmonth,self.endmonth,self.amount)
    class Meta:
        ordering =['acccode']
        verbose_name_plural = "Budget Table"
    def save(self, **kwargs):
        self.acctype = self.acccode.groupcode
        super(tblbudget, self).save(**kwargs)


class tblbudgetmonthly(models.Model):
        acccode = models.ForeignKey(tblaccount)
        startmonth = models.DateField('Start Year')
        endmonth = models.DateField('End Year')
        userid = models.CharField("User Id",max_length = 150,null = False )
        acctype = models.CharField("Account Type",max_length = 150,default='')
        first = models.DecimalField('First',max_digits = 20 , decimal_places = 2, null = True )
        second = models.DecimalField('Second',max_digits = 20 , decimal_places = 2, null = True )
        third = models.DecimalField('Third',max_digits = 20 , decimal_places = 2, null = True )
        four = models.DecimalField('Four',max_digits = 20 , decimal_places = 2, null = True )
        five = models.DecimalField('Five',max_digits = 20 , decimal_places = 2, null = True )
        six = models.DecimalField('six',max_digits = 20 , decimal_places = 2, null = True )
        seven = models.DecimalField('Seven',max_digits = 20 , decimal_places = 2, null = True )
        eight = models.DecimalField('eight',max_digits = 20 , decimal_places = 2, null = True )
        nine = models.DecimalField('nine',max_digits = 20 , decimal_places = 2, null = True )
        ten = models.DecimalField('ten',max_digits = 20 , decimal_places = 2, null = True )
        eleven = models.DecimalField('eleven',max_digits = 20 , decimal_places = 2, null = True )
        twelve = models.DecimalField('twelve',max_digits = 20 , decimal_places = 2, null = True )
        refcode = models.CharField("Ref. Code",max_length = 550,default='')
        def __unicode__(self):
            return  u'%s %s %s %s' % (self.acccode.acccode,self.startmonth,self.endmonth,self.first)
        class Meta:
            ordering =['acccode']
            verbose_name_plural = "Monthly Budget Table"
        def save(self, **kwargs):
            self.acctype = self.acccode.groupcode
            super(tblbudgetmonthly, self).save(**kwargs)

class tblbudgettype(models.Model):
    budget_type = models.CharField("Budget Type",max_length = 550,default='ANNUAL')
    def __unicode__(self):
        return  u'%s' % self.budget_type
    class Meta:
        ordering =['id']
        verbose_name_plural = "Budget Type Table"

