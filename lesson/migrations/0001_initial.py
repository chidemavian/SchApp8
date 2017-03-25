# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'psetup'
        db.create_table('lesson_psetup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('klass', self.gf('django.db.models.fields.CharField')(max_length=130)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=130)),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=130)),
            ('topic', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('num', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('count', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('session', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('lesson', ['psetup'])

        # Adding model 'psetsub'
        db.create_table('lesson_psetsub', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('klass', self.gf('django.db.models.fields.CharField')(default='N/A', max_length=130)),
            ('subject', self.gf('django.db.models.fields.CharField')(default='N/A', max_length=130)),
            ('term', self.gf('django.db.models.fields.CharField')(default='N/A', max_length=130)),
            ('topic', self.gf('django.db.models.fields.CharField')(default='N/A', max_length=2000)),
            ('session', self.gf('django.db.models.fields.CharField')(default='N/A', max_length=15)),
            ('subtopic', self.gf('django.db.models.fields.CharField')(default='N/A', max_length=2000)),
        ))
        db.send_create_signal('lesson', ['psetsub'])

        # Adding model 'Psetweek'
        db.create_table('lesson_psetweek', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lessonperweek', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('klass', self.gf('django.db.models.fields.CharField')(max_length=130)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=130)),
            ('teacherid', self.gf('django.db.models.fields.CharField')(max_length=2000)),
        ))
        db.send_create_signal('lesson', ['Psetweek'])

        # Adding model 'User'
        db.create_table('lesson_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('klass', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('lesson', ['User'])


    def backwards(self, orm):
        # Deleting model 'psetup'
        db.delete_table('lesson_psetup')

        # Deleting model 'psetsub'
        db.delete_table('lesson_psetsub')

        # Deleting model 'Psetweek'
        db.delete_table('lesson_psetweek')

        # Deleting model 'User'
        db.delete_table('lesson_user')


    models = {
        'lesson.psetsub': {
            'Meta': {'object_name': 'psetsub'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '130'}),
            'session': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '15'}),
            'subject': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '130'}),
            'subtopic': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '2000'}),
            'term': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '130'}),
            'topic': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '2000'})
        },
        'lesson.psetup': {
            'Meta': {'object_name': 'psetup'},
            'count': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.CharField', [], {'max_length': '130'}),
            'num': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '130'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '130'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        'lesson.psetweek': {
            'Meta': {'object_name': 'Psetweek'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.CharField', [], {'max_length': '130'}),
            'lessonperweek': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '130'}),
            'teacherid': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        'lesson.user': {
            'Meta': {'object_name': 'User'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        }
    }

    complete_apps = ['lesson']