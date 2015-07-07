from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Admin)
admin.site.register(Client)
admin.site.register(Culprit)
admin.site.register(Event)
admin.site.register(InboundEmail)
admin.site.register(SavedSearch)
admin.site.register(SchemaMigration)
admin.site.register(Share)
admin.site.register(Star)
admin.site.register(Tag)
admin.site.register(Subscription)
admin.site.register(Survey)
admin.site.register(Ticket)
admin.site.register(TagsTicket)
admin.site.register(Webhook)
