from django.views.generic import TemplateView, ListView, DetailView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from main.models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class IndexView(TemplateView):
    template_name = "index.html"

class EventListView(LoginRequiredMixin, ListView):
	'''List of All Events'''
	model = Event
	context_object_name = 'events'
	template_name = 'student_dashboard.html'

	def get_context_data(self, **kwargs):
		user_events = []
		context = super().get_context_data(**kwargs)
		res = ParticipatedEvent.objects.filter(user=self.request.user)
		for r in res:
			user_events.append(r.event)
		context['user_events'] = user_events
		return context

class UserParticipatedView(LoginRequiredMixin,ListView):
	'''Participated Events of User'''
	model = ParticipatedEvent
	context_object_name = 'participated_events'
	template_name = 'student_participated.html'

	def get_queryset(self):
		return ParticipatedEvent.objects.filter(user=self.request.user)

class EventStatusView(TemplateView):
	'''Status of Event on User Dashboard'''
	template_name = 'event_status.html'

class ParticipatedStudentsView(LoginRequiredMixin,UserPassesTestMixin,ListView):
	'''List of Students Participated in Events'''
	model = ParticipatedEvent
	template_name = 'event_details.html'
	context_object_name = 'event_students'

	def test_func(self):
		return self.request.user.groups.filter(name='coordinator').exists()

	def get_queryset(self):
		return ParticipatedEvent.objects.filter(event=self.request.user.member.associated_event)

	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    event_sum = 0
	    result = ParticipatedEvent.objects.filter(event=self.request.user.member.associated_event)
	    for r in result:
	    	if r.payment_status == "Y":
	    		event_sum = event_sum + r.event.price
	    context['event_sum'] = event_sum
	    return context

class StudentParticipationStatusView(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
	'''Status of Participation of Student'''
	template_name = "student_status.html"

	def test_func(self):
		return self.request.user.groups.filter(name='coordinator').exists()

@login_required
def register_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	print(event.name)
	e = ParticipatedEvent(user=request.user, event=event, payment_status='N')
	e.save()
	return render(request, 'event_status.html', {'event':event, 'event_details':e})

@login_required
def approve_student(request, participation_id):
	participation_info = ParticipatedEvent.objects.get(pk=participation_id)
	participation_info.payment_status='Y'
	participation_info.save()
	return redirect('event_details')

@login_required
def get_receipt_participation(request, participation_id):
	participation_info = ParticipatedEvent.objects.get(pk=participation_id)
	if participation_info.payment_status == "N":
		return redirect('student_participated')
	else:
		return render(request, 'participation_receipt.html',{'info':participation_info})