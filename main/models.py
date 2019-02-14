from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
	name = models.CharField(max_length=128, blank=False)
	price = models.FloatField(blank=False)

	def __str__(self):
		return self.name

class Member(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	associated_event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True)

	def __str__(self):
		return self.user.first_name

class ParticipatedEvent(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	payment_status = models.CharField(max_length=1,blank=False)
	approval_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '''{} and {} on {}'''.format(self.user.first_name, self.event.name, self.approval_date)
