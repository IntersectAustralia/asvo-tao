# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TaoUser.disk_quota'
        db.add_column(u'tao_taouser', 'disk_quota',
                      self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Job.disk_usage'
        db.add_column(u'tao_job', 'disk_usage',
                      self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TaoUser.disk_quota'
        db.delete_column(u'tao_taouser', 'disk_quota')

        # Deleting field 'Job.disk_usage'
        db.delete_column(u'tao_job', 'disk_usage')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tao.bandpassfilter': {
            'Meta': {'ordering': "['group', 'order', 'label']", 'object_name': 'BandPassFilter'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'filter_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'tao.dataset': {
            'Meta': {'unique_together': "(('simulation', 'galaxy_model'),)", 'object_name': 'DataSet'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'database': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'default_filter_field': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'DataSetProperty'", 'null': 'True', 'to': u"orm['tao.DataSetProperty']"}),
            'default_filter_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'default_filter_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'galaxy_model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tao.GalaxyModel']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'import_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'job_size_p1': ('django.db.models.fields.FloatField', [], {'default': '0.065550529999999996'}),
            'job_size_p2': ('django.db.models.fields.FloatField', [], {'default': '-0.10355211'}),
            'job_size_p3': ('django.db.models.fields.FloatField', [], {'default': '0.37135452000000002'}),
            'max_job_box_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'simulation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tao.Simulation']"}),
            'version': ('django.db.models.fields.DecimalField', [], {'default': "'1.00'", 'max_digits': '10', 'decimal_places': '2'})
        },
        u'tao.datasetproperty': {
            'Meta': {'ordering': "['group', 'order', 'label']", 'object_name': 'DataSetProperty'},
            'data_type': ('django.db.models.fields.IntegerField', [], {}),
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tao.DataSet']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'flags': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_computed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_filter': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_index': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_output': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'units': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'})
        },
        u'tao.dustmodel': {
            'Meta': {'object_name': 'DustModel'},
            'details': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'tao.galaxymodel': {
            'Meta': {'ordering': "['name']", 'object_name': 'GalaxyModel'},
            'details': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'simulation_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tao.Simulation']", 'through': u"orm['tao.DataSet']", 'symmetrical': 'False'})
        },
        u'tao.globalparameter': {
            'Meta': {'object_name': 'GlobalParameter'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameter_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'parameter_value': ('django.db.models.fields.TextField', [], {'default': "''"})
        },
        u'tao.job': {
            'Meta': {'object_name': 'Job'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'database': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'disk_usage': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'error_message': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1000000', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'output_path': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parameters': ('django.db.models.fields.TextField', [], {'max_length': '1000000', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'SUBMITTED'", 'max_length': '20'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tao.TaoUser']"})
        },
        u'tao.simulation': {
            'Meta': {'ordering': "['order', 'name']", 'object_name': 'Simulation'},
            'box_size': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '3'}),
            'box_size_units': ('django.db.models.fields.CharField', [], {'default': "'Mpc'", 'max_length': '10'}),
            'details': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': "'0'"})
        },
        u'tao.snapshot': {
            'Meta': {'unique_together': "(('dataset', 'redshift'),)", 'object_name': 'Snapshot'},
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tao.DataSet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'redshift': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '10'})
        },
        u'tao.stellarmodel': {
            'Meta': {'object_name': 'StellarModel'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'encoding': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'tao.taouser': {
            'Meta': {'object_name': 'TaoUser'},
            'aaf_shared_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'account_registration_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'account_registration_reason': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'account_registration_status': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '3'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'disk_quota': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'rejected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'scientific_interests': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'tao.workflowcommand': {
            'Meta': {'object_name': 'WorkflowCommand'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'executed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'execution_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'execution_status': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'job_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tao.Job']", 'null': 'True', 'blank': 'True'}),
            'parameters': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'submitted_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tao.TaoUser']"})
        }
    }

    complete_apps = ['tao']