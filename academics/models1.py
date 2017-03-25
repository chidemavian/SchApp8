from django.db import models
from django.db.utils import DatabaseError
from django.db.models import Avg
from django.core.exceptions import FieldError
from myproject.utils import SchoolSessionValidator
from myproject.student.models import Student
from myproject.setup.models import Subject
from myproject.sysadmin.models import *
from myproject.academics.utils import *

# Create your models here.
terms_list = (('First', 'First Term'), ('Second', 'Second Term'), ('Third', 'Third Term'))


class StudentAcademicRecord(models.Model):
    student = models.ForeignKey(Student, related_name='academic_record')
    klass = models.CharField('Class', max_length=20, default='')
    arm = models.CharField('Arm', max_length=10, default='')
    term = models.CharField('Term', max_length=20, choices=terms_list, null=True)
    session = models.CharField('Session', max_length=20, default='', validators=[SchoolSessionValidator])
    days_open = models.IntegerField('No. of Days School Opened', default=0)
    days_present = models.IntegerField('Days Present', default=0)
    days_absent = models.IntegerField('Days Absent', default=0)
    position = models.CharField('Position', max_length=10, default='N/A')
    percentage = models.DecimalField('Percentage', decimal_places=2, max_digits=5, default=0)
    class_teacher_comment = models.CharField("Class Teacher's Comment", max_length=150, default='')
    principal_comment = models.CharField("Principal's Comment", max_length=100, default='')
    next_term_start = models.DateField('Next Term Begins', null=True, default=models.NOT_PROVIDED)

    def __unicode__(self):
        return  u'Name: %s, Admission No: %s , Class: %s, Arm: %s,Session: %s' %(self.student.fullname,self.student.admissionno,self.klass,self.arm,self.session)
    class Meta:
        ordering = ['student']
        verbose_name_plural = 'Student Academic'

    def __get_subjects(self):
        if self.student.subclass.startswith('J'):
            try:
                return [(s.subject, s.num) for s in Subject.objects.filter(category='JS')]
            except DatabaseError:
                return []
        elif self.student.subclass.startswith('A'):
            try:
                return [(s.subject, s.num) for s in Subject.objects.filter(category='Art')]
            except DatabaseError:
                return []
        elif self.student.subclass.startswith('S'):
            try:
                return [(s.subject, s.num) for s in Subject.objects.filter(category='Science')]
            except DatabaseError:
                return []
        elif self.student.subclass.startswith('C'):
            try:
                return [(s.subject, s.num) for s in Subject.objects.filter(category='Commercial')]
            except DatabaseError:
                return []

        else:
            try:
              return [(s.subject, s.num) for s in Subject.objects.exclude(category='Year')]
            except DatabaseError:
               return []
    #def save(self, **kwargs):
     # self.klass = self.student.admitted_class
      #self.arm = self.student.admitted_arm
      #super(StudentAcademicRecord, self).save(**kwargs)
      #  AffectiveSkill(academic_rec=self).save()
       # PsychomotorSkill(academic_rec=self).save()

        #for subject in self.__get_subjects():
         #   SubjectScore(subject=subject[0], academic_rec=self, num=subject[1], term=self.term,
          #              session=self.session, klass=self.klass, arm=self.arm).save()


score = (('A', 'A - Exceptionally Exhibited'), ('B', 'B - Appreciably Demonstrated'),
        ('C', 'C - Satisfactorily Displayed'), ('D', 'D - Needs Improvement'),
        ('N/A', 'Not Available'))


class AffectiveSkill(models.Model):
    academic_rec = models.OneToOneField(StudentAcademicRecord, related_name='affective_domain')
    punctuality = models.CharField('Punctuality', max_length=3, choices=score, default='A')
    neatness = models.CharField('Neatness', max_length=3, choices=score, default='A')
    honesty = models.CharField('Honesty', max_length=3, choices=score, default='A')
    initiative = models.CharField('Initiative', max_length=3, choices=score, default='A')
    self_control = models.CharField('Self Control', max_length=3, choices=score, default='A')
    reliability = models.CharField('Reliability', max_length=3, choices=score, default='A')
    perseverance = models.CharField('Perseverance', max_length=3, choices=score, default='A')
    politeness = models.CharField('Politeness', max_length=3, choices=score, default='A')
    attentiveness = models.CharField('Attentiveness', max_length=3, choices=score, default='A')
    rel_with_people = models.CharField('Relationship with People', max_length=3, choices=score, default='A')
    cooperation = models.CharField('Co-operation', max_length=3, choices=score, default='A')
    organizational_ability = models.CharField('Organizational Ability', max_length=3, choices=score, default='A')

    def __unicode__(self):
        return u'Name :%s,Admission No : %s,Class : %s,Arm %s:Session %s' %(self.academic_rec.student.fullname,self.academic_rec.student.admissionno,self.academic_rec.klass,self.academic_rec.arm,self.academic_rec.session)


class PsychomotorSkill(models.Model):
    academic_rec = models.OneToOneField(StudentAcademicRecord, related_name='psychomotor_domain')
    handwriting = models.CharField('Handwriting', max_length=3, choices=score, default='A')
    games = models.CharField('Games & Sports', max_length=3, choices=score, default='A')
    art = models.CharField('Drawing/Arts', max_length=3, choices=score, default='A')
    painting = models.CharField('Painting', max_length=3, choices=score, default='A')
    music = models.CharField('Musical Skills', max_length=3, choices=score, default='A')

    def __unicode__(self):
        return u'Name :%s,Admission No : %s,Class : %s,Arm %s: ,Session %s' %(self.academic_rec.student.fullname,self.academic_rec.student.admissionno,self.academic_rec.klass,self.academic_rec.arm,self.academic_rec.session)

grading = (('A', 'A (80 - 100)'), ('B', 'B (65 - 79)'), ('C', 'C (55 - 64)'),
           ('P', 'P (45 - 54)'), ('F', 'F (0 - 4)'))


class SubjectScore(models.Model):
    academic_rec = models.ForeignKey(StudentAcademicRecord, related_name='subject_scores')
    subject = models.CharField('Subject', max_length=125, default=0)
    num = models.IntegerField(editable=False)
    term = models.CharField('Term', max_length=20, choices=terms_list)
    session = models.CharField('Session', max_length=20)
    klass = models.CharField('Class', max_length=20)
    arm = models.CharField('Arm', max_length=10)
    first_ca = models.DecimalField('First CA', decimal_places=2, max_digits=5, default=0)
    second_ca = models.DecimalField('Second CA', decimal_places=2, max_digits=5, default=0)
    third_ca = models.DecimalField('Third CA', decimal_places=2, max_digits=5, default=0)
    fourth_ca = models.DecimalField('Fourth CA', decimal_places=2, max_digits=5, default=0)
    fifth_ca = models.DecimalField('Fifth CA', decimal_places=2, max_digits=5, default=0)
    sixth_ca = models.DecimalField('Sixth CA', decimal_places=2, max_digits=5, default=0)
    exam_score = models.DecimalField('Exam', decimal_places=2, max_digits=5, default=0)
    term_score = models.DecimalField('Term Score', decimal_places=2, max_digits=5, default=0)
    grade = models.CharField('Grade', max_length=3, default= 'F')
    subject_avg = models.DecimalField(decimal_places=2, max_digits=6, default=0, editable=False)
    subposition = models.CharField('Position', max_length=10, default='N/A')
    remark = models.CharField('Remark', max_length=60)
    subject_teacher = models.CharField('Subject Teacher', max_length=200,null=True, default=models.NOT_PROVIDED)
    annual_avg = models.DecimalField(decimal_places=2, max_digits=6, default=0, editable=False)

    def __unicode__(self):
        return u'%s %s-%s-%s-%s-%s-%s-%s-%s-%s-%s-%s-%s-%s' %(self.academic_rec.student.subclass, self.term,self.academic_rec.student.fullname,self.academic_rec.student.admissionno,self.academic_rec.klass,self.academic_rec.arm,self.academic_rec.session,self.subject,self.first_ca,self.second_ca,self.exam_score,self.term_score,self.remark,self.annual_avg)
    class Meta:
        ordering = ['academic_rec']
        verbose_name_plural = 'Student Academic Scores Table'

    def save(self, **kwargs):
        fterm = float(self.first_ca) + float(self.second_ca) + float(self.exam_score)
        self.term_score = str(fterm)
        self.arm = self.academic_rec.arm
        self.klass = self.academic_rec.klass
        self.term = self.academic_rec.term
        if self.term.startswith('T'):
            if self.klass.startswith('J'):
               if (float(self.annual_avg) >=70) and (float(self.annual_avg) <= 100):
                   self.grade = 'A'
                   self.remark = 'Excellent'
               elif (float(self.annual_avg) >=50) and (float(self.annual_avg) <= 69.9):
                   self.grade = 'C'
                   self.remark = 'Credit'
               elif (float(self.annual_avg) >=40) and (float(self.annual_avg) <= 49.9):
                   self.grade = 'P'
                   self.remark = 'Pass'
               elif (float(self.annual_avg) >=0) and (float(self.annual_avg) <= 44.9):
                    self.grade = 'F'
                    self.remark = 'Fail'
               else:
                   raise FieldError('Term score cannot exceed 100 or be less than 0!')
               super(SubjectScore, self).save(**kwargs)
            elif self.klass.startswith('S'):
                if (float(self.annual_avg) >=75) and (float(self.annual_avg) <= 100):
                    self.grade = 'A1'
                    self.remark = 'Excellent'
                elif (float(self.annual_avg) >=70) and (float(self.annual_avg) <= 74.9):
                    self.grade = 'B2'
                    self.remark = 'V.Good'
                elif (float(self.annual_avg) >=65) and (float(self.annual_avg) <= 69.9):
                     self.grade = 'B3'
                     self.remark = 'Good'
                elif (float(self.annual_avg) >=60) and (float(self.annual_avg) <= 64.9):
                     self.grade = 'C4'
                     self.remark = 'Credit'
                elif (float(self.annual_avg) >=55) and (float(self.annual_avg) <= 59.9):
                     self.grade = 'C5'
                     self.remark = 'Credit'
                elif (float(self.annual_avg) >=50) and (float(self.annual_avg) <= 54.9):
                      self.grade = 'C6'
                      self.remark = 'Credit'
                elif (float(self.annual_avg) >=45) and (float(self.annual_avg) <= 49.9):
                     self.grade = 'D7'
                     self.remark = 'Pass'
                elif (float(self.annual_avg) >=40) and (float(self.annual_avg) <= 44.9):
                      self.grade = 'E8'
                      self.remark = 'Pass'
                elif (float(self.annual_avg) >=0) and (float(self.annual_avg) <= 39.9):
                     self.grade = 'F9'
                     self.remark = 'Fail'
                else:
                    raise FieldError('Term score cannot exceed 100 or be less than 0!')
                super(SubjectScore, self).save(**kwargs)
            else:
                if (float(self.annual_avg) >=95) and (float(self.annual_avg) <= 100):
                    self.grade = 'A+'
                    self.remark = 'Excellent'
                elif (float(self.annual_avg) >=90) and (float(self.annual_avg) <= 94.9):
                    self.grade = 'A'
                    self.remark = 'Excellent'
                elif (float(self.annual_avg) >=85) and (float(self.annual_avg) <= 89.9):
                    self.grade = 'A-'
                    self.remark = 'Very Good'
                elif (float(self.annual_avg) >=80) and (float(self.annual_avg) <= 84.9):
                    self.grade = 'B+'
                    self.remark = 'Very Good'
                elif (float(self.annual_avg) >=75) and (float(self.annual_avg) <= 79.9):
                    self.grade = 'B'
                    self.remark = 'Good'
                elif (float(self.annual_avg) >=70) and (float(self.annual_avg) <= 74.9):
                    self.grade = 'B-'
                    self.remark = 'Good'
                elif (float(self.annual_avg) >=65) and (float(self.annual_avg) <= 69.9):
                    self.grade = 'C+'
                    self.remark = 'Average'
                elif (float(self.annual_avg) >=60) and (float(self.annual_avg) <= 64.9):
                    self.grade = 'C'
                    self.remark = 'Below Average'
                elif (float(self.annual_avg) >=55) and (float(self.annual_avg) <= 59.9):
                    self.grade = 'C-'
                    self.remark = 'Below Average'
                elif (float(self.annual_avg) >=50) and (float(self.annual_avg) <= 54.9):
                    self.grade = 'D'
                    self.remark = 'Fair'
                elif (float(self.annual_avg) >=45) and (float(self.annual_avg) <= 49.9):
                    self.grade = 'D-'
                    self.remark = 'Poor'
                elif (float(self.annual_avg) >=40) and (float(self.annual_avg) <= 44.9):
                    self.grade = 'E'
                    self.remark = 'Very Poor'
                elif (float(self.annual_avg) >=0) and (float(self.annual_avg) <= 39.9):
                    self.grade = 'F'
                    self.remark = 'Fail'
                else:
                    raise FieldError('Term score cannot exceed 100 or be less than 0!')
                super(SubjectScore, self).save(**kwargs)

        else:
           if self.klass.startswith('J'):
               if (float(self.term_score) >=70) and (float(self.term_score) <= 100):
                   self.grade = 'A'
                   self.remark = 'Excellent'
               elif (float(self.term_score) >=50) and (float(self.term_score) <= 69.9):
                   self.grade = 'C'
                   self.remark = 'Credit'
               elif (float(self.term_score) >=40) and (float(self.term_score) <= 49.9):
                   self.grade = 'P'
                   self.remark = 'Pass'
               elif (float(self.term_score) >=0) and (float(self.term_score) <= 44.9):
                   self.grade = 'F'
                   self.remark = 'Fail'
               else:
                   raise FieldError('Term score cannot exceed 100 or be less than 0!')
               super(SubjectScore, self).save(**kwargs)
           elif self.klass.startswith('S'):
               if (float(self.term_score) >=75) and (float(self.term_score) <= 100):
                   self.grade = 'A1'
                   self.remark = 'Excellent'
               elif (float(self.term_score) >=70) and (float(self.term_score) <= 74.9):
                   self.grade = 'B2'
                   self.remark = 'V.Good'
               elif (float(self.term_score) >=65) and (float(self.term_score) <= 69.9):
                   self.grade = 'B3'
                   self.remark = 'Good'
               elif (float(self.term_score) >=60) and (float(self.term_score) <= 64.9):
                   self.grade = 'C4'
                   self.remark = 'Credit'
               elif (float(self.term_score) >=55) and (float(self.term_score) <= 59.9):
                   self.grade = 'C5'
                   self.remark = 'Credit'
               elif (float(self.term_score) >=50) and (float(self.term_score) <= 54.9):
                   self.grade = 'C6'
                   self.remark = 'Credit'
               elif (float(self.term_score) >=45) and (float(self.term_score) <= 49.9):
                   self.grade = 'D7'
                   self.remark = 'Pass'
               elif (float(self.term_score) >=40) and (float(self.term_score) <= 44.9):
                   self.grade = 'E8'
                   self.remark = 'Pass'
               elif (float(self.term_score) >=0) and (float(self.term_score) <= 39.9):
                   self.grade = 'F9'
                   self.remark = 'Fail'
               else:
                   raise FieldError('Term score cannot exceed 100 or be less than 0!')
               super(SubjectScore, self).save(**kwargs)
           else:
               if (float(self.term_score) >=95) and (float(self.term_score) <= 100):
                   self.grade = 'A+'
                   self.remark = 'Excellent'
               elif (float(self.term_score) >=90) and (float(self.term_score) <= 94.9):
                   self.grade = 'A'
                   self.remark = 'Excellent'
               elif (float(self.term_score) >=85) and (float(self.term_score) <= 89.9):
                   self.grade = 'A-'
                   self.remark = 'Very Good'
               elif (float(self.term_score) >=80) and (float(self.term_score) <= 84.9):
                   self.grade = 'B+'
                   self.remark = 'Very Good'
               elif (float(self.term_score) >=75) and (float(self.term_score) <= 79.9):
                    self.grade = 'B'
                    self.remark = 'Good'
               elif (float(self.term_score) >=70) and (float(self.term_score) <= 74.9):
                    self.grade = 'B-'
                    self.remark = 'Good'
               elif (float(self.term_score) >=65) and (float(self.term_score) <= 69.9):
                     self.grade = 'C+'
                     self.remark = 'Average'
               elif (float(self.term_score) >=60) and (float(self.term_score) <= 64.9):
                     self.grade = 'C'
                     self.remark = 'Below Average'
               elif (float(self.term_score) >=55) and (float(self.term_score) <= 59.9):
                    self.grade = 'C-'
                    self.remark = 'Below Average'
               elif (float(self.term_score) >=50) and (float(self.term_score) <= 54.9):
                     self.grade = 'D'
                     self.remark = 'Fair'
               elif (float(self.term_score) >=45) and (float(self.term_score) <= 49.9):
                    self.grade = 'D-'
                    self.remark = 'Poor'
               elif (float(self.term_score) >=40) and (float(self.term_score) <= 44.9):
                   self.grade = 'E'
                   self.remark = 'Very Poor'
               elif (float(self.term_score) >=0) and (float(self.term_score) <= 39.9):
                     self.grade = 'F'
                     self.remark = 'Fail'
               else:
                     raise FieldError('Term score cannot exceed 100 or be less than 0!')
               super(SubjectScore, self).save(**kwargs)



