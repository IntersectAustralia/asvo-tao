# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ActivityRecord'
        db.create_table(u'activitylog_activityrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('session_id', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('request_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tao.TaoUser'])),
            ('request_path', self.gf('django.db.models.fields.TextField')()),
            ('request_query_string', self.gf('django.db.models.fields.TextField')()),
            ('request_vars', self.gf('django.db.models.fields.TextField')()),
            ('request_method', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('request_secure', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('request_ajax', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('request_meta', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('request_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('view_function', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('view_doc_string', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('view_args', self.gf('django.db.models.fields.TextField')()),
            ('response_code', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('response_content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'activitylog', ['ActivityRecord'])


    def backwards(self, orm):
        # Deleting model 'ActivityRecord'
        db.delete_table(u'activitylog_activityrecord')


    models = {
        u'activitylog.activityrecord': {
            'Meta': {'object_name': 'ActivityRecord'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'request_ajax': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'request_meta': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'request_method': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'request_path': ('django.db.models.fields.TextField', [], {}),
            'request_query_string': ('django.db.models.fields.TextField', [], {}),
            'request_secure': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'request_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tao.TaoUser']"}),
            'request_vars': ('django.db.models.fields.TextField', [], {}),
            'response_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'response_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'session_id': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'view_args': ('django.db.models.fields.TextField', [], {}),
            'view_doc_string': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'view_function': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
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
        u'tao.taouser': {
            'Meta': {'object_name': 'TaoUser'},
            'aaf_shared_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'account_registration_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'account_registration_reason': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'account_registration_status': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '3'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
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
        }
    }

    complete_apps = ['activitylog']