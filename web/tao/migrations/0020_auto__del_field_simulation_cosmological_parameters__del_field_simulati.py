# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Simulation.cosmological_parameters'
        db.delete_column('tao_simulation', 'cosmological_parameters')

        # Deleting field 'Simulation.paper_url'
        db.delete_column('tao_simulation', 'paper_url')

        # Deleting field 'Simulation.web_site'
        db.delete_column('tao_simulation', 'web_site')

        # Deleting field 'Simulation.cosmology'
        db.delete_column('tao_simulation', 'cosmology')

        # Deleting field 'Simulation.external_link_url'
        db.delete_column('tao_simulation', 'external_link_url')

        # Deleting field 'Simulation.paper_title'
        db.delete_column('tao_simulation', 'paper_title')

        # Adding field 'Simulation.details'
        db.add_column('tao_simulation', 'details',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Simulation.cosmological_parameters'
        db.add_column('tao_simulation', 'cosmological_parameters',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Simulation.paper_url'
        db.add_column('tao_simulation', 'paper_url',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Simulation.web_site'
        db.add_column('tao_simulation', 'web_site',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Simulation.cosmology'
        db.add_column('tao_simulation', 'cosmology',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Simulation.external_link_url'
        db.add_column('tao_simulation', 'external_link_url',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Simulation.paper_title'
        db.add_column('tao_simulation', 'paper_title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Deleting field 'Simulation.details'
        db.delete_column('tao_simulation', 'details')


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
        'tao.dataset': {
            'Meta': {'unique_together': "(('simulation', 'galaxy_model'),)", 'object_name': 'DataSet'},
            'database': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'galaxy_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tao.GalaxyModel']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'simulation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tao.Simulation']"})
        },
        'tao.datasetparameter': {
            'Meta': {'object_name': 'DataSetParameter'},
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tao.DataSet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'tao.galaxymodel': {
            'Meta': {'ordering': "['name']", 'object_name': 'GalaxyModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'paper_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'paper_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'}),
            'simulation_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tao.Simulation']", 'through': "orm['tao.DataSet']", 'symmetrical': 'False'})
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
            'Meta': {'ordering': "['name']", 'object_name': 'Simulation'},
            'box_size': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '3'}),
            'box_size_units': ('django.db.models.fields.CharField', [], {'default': "'Mpc'", 'max_length': '10'}),
            'details': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'tao.snapshot': {
            'Meta': {'unique_together': "(('dataset', 'redshift'),)", 'object_name': 'Snapshot'},
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tao.DataSet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'redshift': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '5'})
        },
        'tao.stellarmodel': {
            'Meta': {'object_name': 'StellarModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
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