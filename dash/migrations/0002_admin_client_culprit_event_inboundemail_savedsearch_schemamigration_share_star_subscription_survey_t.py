# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('user_id', models.UUIDField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'admins',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('token', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'clients',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Culprit',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('ticket_id', models.IntegerField(blank=True, null=True)),
                ('tag_id', models.UUIDField(blank=True, null=True)),
                ('reason', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('actor_id', models.UUIDField()),
            ],
            options={
                'db_table': 'culprits',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('type', models.TextField()),
                ('body', models.TextField(blank=True, null=True)),
                ('public', models.NullBooleanField()),
                ('change', models.TextField(blank=True, null=True)),
                ('actor_id', models.UUIDField(blank=True, null=True)),
                ('client_id', models.UUIDField(blank=True, null=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('user_cache', models.TextField(blank=True, null=True)),
                ('meta_data', models.TextField(blank=True, null=True)),
                ('body_html', models.TextField(blank=True, null=True)),
                ('sfid', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'events',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='InboundEmail',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('payload', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('message_id', models.TextField(unique=True)),
                ('processed_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'inbound_emails',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SavedSearch',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('user_id', models.UUIDField()),
                ('name', models.TextField()),
                ('search', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'saved_searches',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SchemaMigration',
            fields=[
                ('filename', models.TextField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'schema_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('user_id', models.UUIDField(blank=True, null=True)),
                ('ticket_id', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'shares',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('user_id', models.UUIDField(blank=True, null=True)),
                ('ticket_id', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'stars',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('user_id', models.UUIDField(blank=True, null=True)),
                ('notify', models.NullBooleanField()),
                ('client_id', models.UUIDField(blank=True, null=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'subscriptions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('ticket_id', models.IntegerField(blank=True, unique=True, null=True)),
                ('support_score', models.IntegerField(blank=True, null=True)),
                ('platform_score', models.IntegerField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('actor_id', models.UUIDField()),
                ('client_id', models.UUIDField(blank=True, null=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'surveys',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('slug', models.TextField()),
                ('kind', models.TextField()),
                ('external_id', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('addon', models.NullBooleanField()),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('surveyable', models.NullBooleanField()),
                ('meta_data', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tags',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TagsTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'tags_tickets',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.FloatField(primary_key=True, serialize=False)),
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
            name='Webhook',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('uri', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('triggered_at', models.DateTimeField(blank=True, null=True)),
                ('enabled', models.NullBooleanField()),
                ('token', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'webhooks',
                'managed': False,
            },
        ),
    ]
