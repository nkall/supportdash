# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
import uuid

class Admins(models.Model):
    id = models.UUIDField(primary_key=True)
    user_id = models.UUIDField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admins'


class Clients(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    token = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clients'


class Culprits(models.Model):
    id = models.UUIDField(primary_key=True)
    ticket_id = models.IntegerField(blank=True, null=True)
    tag_id = models.UUIDField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    actor_id = models.UUIDField()

    class Meta:
        managed = False
        db_table = 'culprits'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Events(models.Model):
    id = models.UUIDField(primary_key=True)
    type = models.TextField()
    body = models.TextField(blank=True, null=True)
    public = models.NullBooleanField()
    change = models.TextField(blank=True, null=True)
    actor_id = models.UUIDField(blank=True, null=True)
    client_id = models.UUIDField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    user_cache = models.TextField(blank=True, null=True)
    meta_data = models.TextField(blank=True, null=True)
    body_html = models.TextField(blank=True, null=True)
    sfid = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'events'


class InboundEmails(models.Model):
    id = models.UUIDField(primary_key=True)
    payload = models.TextField()
    created_at = models.DateTimeField()
    message_id = models.TextField(unique=True)
    processed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inbound_emails'


class SavedSearches(models.Model):
    id = models.UUIDField(primary_key=True)
    user_id = models.UUIDField()
    name = models.TextField()
    search = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'saved_searches'


class SchemaMigrations(models.Model):
    filename = models.TextField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'schema_migrations'


class Shares(models.Model):
    id = models.UUIDField(primary_key=True)
    user_id = models.UUIDField(blank=True, null=True)
    ticket_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shares'


class Stars(models.Model):
    id = models.UUIDField(primary_key=True)
    user_id = models.UUIDField(blank=True, null=True)
    ticket_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stars'

class Tags(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.TextField()
    slug = models.TextField()
    kind = models.TextField()
    external_id = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    addon = models.NullBooleanField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    surveyable = models.NullBooleanField()
    meta_data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tags'


class Subscriptions(models.Model):
    id = models.UUIDField(primary_key=True)
    user_id = models.UUIDField(blank=True, null=True)
    tag_id = models.ForeignKey(Tags, blank=True, null=True)
    notify = models.NullBooleanField()
    client_id = models.UUIDField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subscriptions'


class Surveys(models.Model):
    id = models.UUIDField(primary_key=True)
    ticket_id = models.IntegerField(unique=True, blank=True, null=True)
    support_score = models.IntegerField(blank=True, null=True)
    platform_score = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    actor_id = models.UUIDField()
    client_id = models.UUIDField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'surveys'

class Tickets(models.Model):
    id = models.FloatField(primary_key=True)
    state = models.TextField()
    app_name = models.TextField()
    salesforce_contact_user_id = models.TextField()
    requester_id = models.TextField()
    actor_id = models.TextField()
    category = models.TextField()
    priority = models.TextField()
    permission_granted_at = models.DateTimeField()
    client_id = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()
    assignee_id = models.TextField()
    subject = models.TextField()
    meta_data = models.TextField()
    state_changed_at = models.DateTimeField()
    stale_notified_at = models.DateTimeField()
    addon = models.TextField()
    last_public_change_at = models.DateTimeField()
    customer_comments_count = models.FloatField()
    salesforce_app_id = models.FloatField()

    class Meta:
        managed = False
        db_table = 'tickets'

class TagsTickets(models.Model):
    tag_id = models.ForeignKey(Tags)
    ticket_id = models.ForeignKey(Tickets)

    class Meta:
        managed = False
        db_table = 'tags_tickets'
        unique_together = (('tag_id', 'ticket_id'),)


class Webhooks(models.Model):
    id = models.UUIDField(primary_key=True)
    uri = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    triggered_at = models.DateTimeField(blank=True, null=True)
    enabled = models.NullBooleanField()
    token = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'webhooks'
