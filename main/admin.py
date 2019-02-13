from django.contrib import admin
from main.models import *
# Register your models here.

class DisplayEvent(admin.ModelAdmin):
	list_display = ('id','name','price')
	search_fields = ['name', 'price']
	list_filter = ('name', 'price')

class DisplayParticipatedEvent(admin.ModelAdmin):
	list_display = ('user','event','payment_status')
	search_fields = ['user', 'event']
	list_filter = ('user', 'event','payment_status')

class DisplayMember(admin.ModelAdmin):
	list_display = ('user','associated_event')
	search_fields = ['user', 'associated_event']
	list_filter = ('user', 'associated_event')

admin.site.register(Event, DisplayEvent)
admin.site.register(ParticipatedEvent, DisplayParticipatedEvent)
admin.site.register(Member, DisplayMember)
