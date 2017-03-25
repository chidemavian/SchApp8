from django.db import models
from PIL import Image

# Create your models here.

class useracc(models.Model):
    email = models.CharField('Email', max_length=150)
    password = models.CharField('Password', max_length=150)
    name = models.CharField('Name',max_length= 300)
    photo = models.ImageField('Forum Photo', upload_to='forum', null=True, blank=True, editable=True)
    created = models.DateTimeField('Created Date', auto_now=True)
    active = models.CharField('Activated Account',max_length= 10)
    control = models.CharField('Control Session',max_length= 500)

    def __unicode__(self):
        return  "%s %s" %(self.email,self.name)

    def save(self, size=(60, 60), **kwargs):
        """
	Save Photo after ensuring it is not blank. Resize as needed.
	"""

        if not self.id and not self.photo:
            return

        super(useracc, self).save(**kwargs)

        filename = self.photo.path
        image = Image.open(filename)

        image.thumbnail(size, Image.ANTIALIAS)
        image.save(filename)

    class Meta:
        verbose_name_plural = 'Forum User Account'
        ordering = ['-created', 'email']

class post(models.Model):
    user = models.CharField('user account',max_length= 220)
    comment = models.TextField('comment')
    created = models.DateTimeField('Created Date', auto_now=True)
    postid = models.CharField('Post Id',max_length=750)
    recdate = models.DateField('Filter Date', default='2015-8-11',auto_now=True)

    def __unicode__(self):
        return  "%s %s" %(self.comment,self.user)

    class Meta:
      verbose_name_plural = 'Post '
      ordering = ['-created']


class subcomments(models.Model):
    commentid = models.CharField('Post Id',max_length=750)
    user = models.CharField('user account',max_length= 220)
    comment = models.TextField('comment')
    created = models.DateTimeField('Created Date', auto_now=True)

    def __unicode__(self):
        return  "%s %s" %(self.comment,self.user)

    class Meta:
        verbose_name_plural = 'Sub Post '
        ordering = ['-created']
