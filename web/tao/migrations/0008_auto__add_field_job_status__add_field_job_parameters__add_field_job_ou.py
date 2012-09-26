# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Job.status'
        db.add_column('tao_job', 'status',
                      self.gf('django.db.models.fields.CharField')(default='SUBMITTED', max_length=20),
                      keep_default=False)

        # Adding field 'Job.parameters'
        db.add_column('tao_job', 'parameters',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=1000000, blank=True),
                      keep_default=False)

        # Adding field 'Job.output_path'
        db.add_column('tao_job', 'output_path',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Job.status'
        db.delete_column('tao_job', 'status')

        # Deleting field 'Job.parameters'
        db.delete_column('tao_job', 'parameters')

        # Deleting field 'Job.output_path'
        db.delete_column('tao_job', 'output_path')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'tao.galaxymodel': {
            'Meta': {'object_name': 'GalaxyModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'paper_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'paper_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'}),
            'simulation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tao.Simulation']"})
        },
        'tao.job': {
            'Meta': {'object_name': 'Job'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'output_path': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parameters': ('django.db.models.fields.TextField', [], {'max_length': '1000000', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'SUBMITTED'", 'max_length': '20'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'tao.simulation': {
            'Meta': {'object_name': 'Simulation'},
            'box_size': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'cosmological_parameters': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'cosmology': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'external_link_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'paper_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'paper_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'}),
            'web_site': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'})
        },
        'tao.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rejected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'scientific_interests': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['tao']