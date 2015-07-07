# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admins',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True)),
                ('user_id', models.UUIDField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'admins',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True)),
                ('name', models.TextField(null=True, blank=True)),
                ('token', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(null=True, blank=True)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'clients',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Culprits',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True)),
                ('ticket_id', models.IntegerField(null=True, blank=True)),
                ('tag_id', models.UUIDField(null=True, blank=True)),
                ('reason', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(null=True, blank=True)),
                ('actor_id', models.UUIDField()),
            ],
            options={
                'db_table': 'culprits',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True)),
                ('type', models.TextField()),
                ('body', models.TextField(null=True, blank=True)),
                ('public', models.NullBooleanField()),
                ('change', models.TextField(null=True, blank=True)),
                ('actor_id', models.UUIDField(null=True, blank=True)),
                ('client_id', models.UUIDField(null=True, blank=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(null=True, blank=True)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('user_cache', models.TextField(null=True, blank=True)),
                ('meta_data', models.TextField(null=True, blank=True)),
                ('body_html', models.TextField(null=True, blank=True)),
                ('sfid', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'events',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='InboundEmails',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True)),
                ('payload', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('message_id', models.TextField(unique=True)),
                ('processed_at', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'inbound_emails',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SavedSearches',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True)),
                ('user_id', models.UUIDField()),
                ('name', models.TextField()),
                ('search', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'saved_searches',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SchemaMigrations',
            fields=[
                ('filename', models.TextField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'schema_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Shares',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True)),
                ('user_id', models.UUIDField(null=True, blank=True)),
                ('ticket_id', models.IntegerField(null=True, blank=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'shares',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Stars',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True)),
                ('user_id', models.UUIDField(null=True, blank=True)),
                ('ticket_id', models.IntegerField(null=True, blank=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(null=True, blank=True)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'stars',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True)),
                ('user_id', models.UUIDField(null=True, blank=True)),
                ('notify', models.NullBooleanField()),
                ('client_id', models.UUIDField(null=True, blank=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'subscriptions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Surveys',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True)),
                ('ticket_id', models.IntegerField(null=True, unique=True, blank=True)),
                ('support_score', models.IntegerField(null=True, blank=True)),
                ('platform_score', models.IntegerField(null=True, blank=True)),
                ('comments', models.TextField(null=True, blank=True)),
                ('actor_id', models.UUIDField()),
                ('client_id', models.UUIDField(null=True, blank=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'surveys',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True)),
                ('name', models.TextField()),
                ('slug', models.TextField()),
                ('kind', models.TextField()),
                ('external_id', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(null=True, blank=True)),
                ('addon', models.NullBooleanField()),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('surveyable', models.NullBooleanField()),
                ('meta_data', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'tags',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TagsTickets',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
            ],
            options={
                'db_table': 'tags_tickets',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.FloatField(serialize=False, primary_key=True)),
                ('state', models.TextField()),
                ('app_name', models.TextField()),
                ('salesforce_contact_user_id', models.TextField()),
                ('requester_id', models.TextField()),
                ('actor_id', models.TextField()),
                ('category', models.TextField()),
                ('priority', models.TextField()),
                ('permission_granted_at', models.DateTimeField()),
                ('client_id', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('deleted_at', models.DateTimeField()),
                ('assignee_id', models.TextField()),
                ('subject', models.TextField()),
                ('meta_data', models.TextField()),
                ('state_changed_at', models.DateTimeField()),
                ('stale_notified_at', models.DateTimeField()),
                ('addon', models.TextField()),
                ('last_public_change_at', models.DateTimeField()),
                ('customer_comments_count', models.FloatField()),
                ('salesforce_app_id', models.FloatField()),
            ],
            options={
                'db_table': 'tickets',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Webhooks',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True)),
                ('uri', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(null=True, blank=True)),
                ('triggered_at', models.DateTimeField(null=True, blank=True)),
                ('enabled', models.NullBooleanField()),
                ('token', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'webhooks',
                'managed': False,
            },
        ),
    ]
