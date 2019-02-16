from django.views.generic import TemplateView, ListView, DetailView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from main.models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class IndexView(TemplateView):
    template_name = "index.html"

class DashboardIndex(LoginRequiredMixin, ListView):
	model = Coordinator
	template_name = "coordinator_index.html"
	context_object_name = 'coordinators'

	def get_queryset(self):
		if self.request.user.groups.filter(name='coordinator').exists():
			return Coordinator.objects.filter(associated_event=self.request.user.coordinator.associated_event)
		else:
			return None

class EventListView(LoginRequiredMixin, ListView):
	'''List of All Events'''
	model = Event
	context_object_name = 'events'
	template_name = 'student_dashboard.html'

	def get_context_data(self, **kwargs):
		user_events = {}
		context = super().get_context_data(**kwargs)
		res = ParticipatedEvent.objects.filter(user=self.request.user.participant)
		for r in res:
			user_events[r.event.name] = r.payment_status
		print(user_events)
		context['user_events'] = user_events
		return context

class UserParticipatedView(LoginRequiredMixin,ListView):
	'''Participated Events of User'''
	model = ParticipatedEvent
	context_object_name = 'participated_events'
	template_name = 'student_participated.html'

	def get_queryset(self):
		return ParticipatedEvent.objects.filter(user=self.request.user.participant)

class ParticipatedStudentsView(LoginRequiredMixin,UserPassesTestMixin,ListView):
	'''List of Students Participated in Events'''
	model = ParticipatedEvent
	template_name = 'event_details.html'
	context_object_name = 'event_students'

	def test_func(self):
		return self.request.user.groups.filter(name='coordinator').exists()

	def get_queryset(self):
		return ParticipatedEvent.objects.filter(event=self.request.user.coordinator.associated_event)

	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    event_sum = 0
	    result = ParticipatedEvent.objects.filter(event=self.request.user.coordinator.associated_event)
	    for r in result:
	    	if r.payment_status == "Y":
	    		event_sum = event_sum + r.event.price
	    context['event_sum'] = event_sum
	    return context

	def test_func(self):
		return self.request.user.groups.filter(name='coordinator').exists()

class ApprovedStudentsView(LoginRequiredMixin,UserPassesTestMixin,ListView):
	'''List of Students Approved in Events'''
	model = ParticipatedEvent
	template_name = 'approved_students.html'
	context_object_name = 'approved_students'

	def test_func(self):
		return self.request.user.groups.filter(name='coordinator').exists()

	def get_queryset(self):
		return ParticipatedEvent.objects.filter(event=self.request.user.coordinator.associated_event)

	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    event_sum = 0
	    result = ParticipatedEvent.objects.filter(event=self.request.user.coordinator.associated_event)
	    for r in result:
	    	if r.payment_status == "Y":
	    		event_sum = event_sum + r.event.price
	    context['event_sum'] = event_sum
	    return context

	def test_func(self):
		return self.request.user.groups.filter(name='coordinator').exists()

class SendNotification(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
	template_name = 'send_notification.html'

	def test_func(self):
		return self.request.user.groups.filter(name='coordinator').exists()

	def post(self, request):
		form = request.POST
		event=request.user.coordinator.associated_event
		n = Notification(event=event,message=form['message'])
		n.save()
		return render(request, self.template_name,{'status': 'Y'})

class Register(TemplateView):
	template_name = "registration/register.html"

	def post(self, request):
		form = request.POST
		
		user, created = User.objects.get_or_create(username=form['username'],
												   first_name = form['name'],email=form['email'])
		if created:
			user.set_password(form['password'])
			user.save()
		p = Participant(user=user,college=form['college'],mobile_number=form['number'],
						roll_no=form['roll_no'],year=form['year'],branch=form['branch'])
		p.save()
		return redirect('login')

@login_required
def register_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	print(event.name)
	e = ParticipatedEvent(user=request.user.participant, event=event, payment_status='N')
	e.save()
	return redirect('get_receipt', participation_id=e.pk)

@login_required
def approve_student(request, participation_id):
	participation_info = ParticipatedEvent.objects.get(pk=participation_id)
	participation_info.payment_status='Y'
	participation_info.approvar = request.user.coordinator
	participation_info.save()

	return redirect('event_details')

@login_required
def get_receipt_participation(request, participation_id):
	participation_info = ParticipatedEvent.objects.get(pk=participation_id)
	return render(request, 'participation_receipt.html',{'info':participation_info})
