from django.urls import path
from main.views import *

urlpatterns = [
	path('',IndexView.as_view(),name='index'),
	path('dindex', DashboardIndex.as_view(), name='dindex'),
	path('user_dashboard',EventListView.as_view(),name='user_dashboard'),
	path('student_participated', UserParticipatedView.as_view(), name='student_participated'),
	path('register_event/<int:event_id>',register_event, name='register_event'),
	path('approve_student/<int:participation_id>', approve_student, name='approve_student'),
	path('event_details', ParticipatedStudentsView.as_view(), name='event_details'),
	path('get_receipt/<int:participation_id>', get_receipt_participation, name='get_receipt'),
	path('register', Register.as_view(), name='register'),
	path('approve_students', ApprovedStudentsView.as_view(), name='approve_students'),
	path('send_notification', SendNotification.as_view(), name='send_notification'),
]