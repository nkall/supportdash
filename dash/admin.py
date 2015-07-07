from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Admins)
admin.site.register(Clients)
admin.site.register(Culprits)
admin.site.register(Events)
admin.site.register(InboundEmails)
admin.site.register(SavedSearches)
admin.site.register(SchemaMigrations)
admin.site.register(Shares)
admin.site.register(Stars)
admin.site.register(Tags)
admin.site.register(Subscriptions)
admin.site.register(Surveys)
admin.site.register(Tickets)
admin.site.register(TagsTickets)
admin.site.register(Webhooks)
