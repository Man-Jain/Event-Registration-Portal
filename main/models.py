from django.db import models
from django.contrib.auth.models import User

BRANCH_CHOICES = (('Civil','Civil'),('Mechanical','Mechanical'),('ECE','ECE'),('CS','CS'),('IT','IT'),('EE','EE'),('Others','Others'))
# Create your models here.
class Event(models.Model):
	name = models.CharField(max_length=128, blank=False)
	price = models.FloatField(blank=False)
	toi = models.CharField(choices=(('team','Team Event'),('single','Individual Event')),max_length=128)
	image = models.ImageField(upload_to='img')
	desc = models.TextField()

	def __str__(self):
		return self.name

class Coordinator(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	associated_event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True)
	mobile_number = models.CharField(max_length=128)
	year = models.CharField(max_length=128,choices=(('1','1st Year'),('2','2nd Year'),('3','3rd Year'),('4','4th Year')))
	branch = models.CharField(max_length=128,choices=BRANCH_CHOICES)

	def __str__(self):
		return self.user.first_name

class Participant(models.Model):
	BRANCH_CHOICES = (('Civil','Civil'),('Mechanical','Mechanical'),('ECE','ECE'),('CS','CS'),('IT','IT'),('EE','EE'),('Others','Others'))
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	college = models.CharField(max_length=128)
	mobile_number = models.CharField(max_length=128)
	roll_no = models.CharField(max_length=128)
	year = models.CharField(max_length=128,choices=(('1','1st Year'),('2','2nd Year'),('3','3rd Year'),('4','4th Year')))
	branch = models.CharField(max_length=128,choices=BRANCH_CHOICES)

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

class Notification(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	message = models.CharField(max_length=128)

	def __str__(self):
		return self.event.name