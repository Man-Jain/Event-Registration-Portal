from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
	name = models.CharField(max_length=128, blank=False)
	price = models.FloatField(blank=False)

	def __str__(self):
		return self.name

class Coordinator(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	associated_event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True)

	def __str__(self):
		return self.user.first_name

class Participant(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	college = models.CharField(max_length=128)
	mobile_number = models.CharField(max_length=128)

	def __str__(self):
		return self.user.first_name

class ParticipatedEvent(models.Model):
	user = models.ForeignKey(Participant, on_delete=models.CASCADE)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	payment_status = models.CharField(max_length=1, blank=False)
	approval_date = models.DateTimeField(auto_now=True)
	approvar = models.ForeignKey(Coordinator, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return self.event.name