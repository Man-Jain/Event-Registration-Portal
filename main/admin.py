from django.contrib import admin
from main.models import *
from datetime import time, datetime
from django.http import HttpResponse

from reportlab.lib import colors, units
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


# Register your models here.

class DisplayEvent(admin.ModelAdmin):
	def export_audits_as_pdf(self, request, queryset):
		file_name = "audit_entries{}.pdf".format('hello')
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="{0}"'.format(file_name)
		data = [['name', 'price']]
		for d in queryset.all():
			item = [d.name, d.price,]
			data.append(item)
		doc = SimpleDocTemplate(response, pagesize=(21*units.inch, 29*units.inch))
		elements = []
		table_data = Table(data)
		table_data.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                    ("FONTSIZE",  (0, 0), (-1, -1), 13)]))
		elements.append(table_data)
		doc.build(elements)
		return response

	list_display = ('id','name','price')
	search_fields = ['name', 'price']
	list_filter = ('name', 'price')
	actions = [export_audits_as_pdf]

class DisplayParticipatedEvent(admin.ModelAdmin):
	list_display = ('user','event','payment_status',)
	search_fields = ['user', 'event']
	list_filter = ('user', 'event','payment_status')

class DisplayMember(admin.ModelAdmin):
	list_display = ('user','associated_event')
	search_fields = ['user', 'associated_event']
	list_filter = ('user', 'associated_event')

admin.site.register(Event, DisplayEvent)
admin.site.register(ParticipatedEvent, DisplayParticipatedEvent)
admin.site.register(Coordinator, DisplayMember)
admin.site.register(Participant)
admin.site.register(Notification)
admin.site.register(Team)
