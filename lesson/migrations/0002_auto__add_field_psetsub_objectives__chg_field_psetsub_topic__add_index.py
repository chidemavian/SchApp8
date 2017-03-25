# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'psetsub.objectives'
        db.add_column('lesson_psetsub', 'objectives',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=2000, blank=True),
                      keep_default=False)


        # Renaming column for 'psetsub.topic' to match new field type.
        db.rename_column('lesson_psetsub', 'topic', 'topic_id')
        # Changing field 'psetsub.topic'
        db.alter_column('lesson_psetsub', 'topic_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lesson.psetup']))
        # Adding index on 'psetsub', fields ['topic']
        db.create_index('lesson_psetsub', ['topic_id'])


    def backwards(self, orm):
        # Removing index on 'psetsub', fields ['topic']
        db.delete_index('lesson_psetsub', ['topic_id'])

        # Deleting field 'psetsub.objectives'
        db.delete_column('lesson_psetsub', 'objectives')


        # Renaming column for 'psetsub.topic' to match new field type.
        db.rename_column('lesson_psetsub', 'topic_id', 'topic')
        # Changing field 'psetsub.topic'
        db.alter_column('lesson_psetsub', 'topic', self.gf('django.db.models.fields.CharField')(max_length=2000))

    models = {
        'lesson.psetsub': {
            'Meta': {'object_name': 'psetsub'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '130'}),
            'objectives': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'session': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '15'}),
            'subject': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '130'}),
            'subtopic': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '2000'}),
            'term': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '130'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Topic'", 'to': "orm['lesson.psetup']"})
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