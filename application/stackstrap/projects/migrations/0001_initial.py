# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Template'
        db.create_table(u'projects_template', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('git_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('git_ref', self.gf('django.db.models.fields.CharField')(default='master', max_length=64)),
            ('last_cache_update', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'projects', ['Template'])

        # Adding model 'Box'
        db.create_table(u'projects_box', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255)),
        ))
        db.send_create_signal(u'projects', ['Box'])

        # Adding model 'Project'
        db.create_table(u'projects_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('box', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Box'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='projects', null=True, to=orm['projects.Template'])),
            ('public_key', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('private_key', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'projects', ['Project'])


    def backwards(self, orm):
        # Deleting model 'Template'
        db.delete_table(u'projects_template')

        # Deleting model 'Box'
        db.delete_table(u'projects_box')

        # Deleting model 'Project'
        db.delete_table(u'projects_project')


    models = {
        u'projects.box': {
            'Meta': {'object_name': 'Box'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'box': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Box']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'private_key': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'public_key': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'projects'", 'null': 'True', 'to': u"orm['projects.Template']"})
        },
        u'projects.template': {
            'Meta': {'object_name': 'Template'},
            'git_ref': ('django.db.models.fields.CharField', [], {'default': "'master'", 'max_length': '64'}),
            'git_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_cache_update': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['projects']