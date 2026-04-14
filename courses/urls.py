from django.urls import path
from . import views

urlpatterns = [

    path('', views.course_list, name='course_list'),
    path('add/', views.add_course, name='add_course'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:pk>/register_student/', views.register_student, name='register_student'),
    path('<int:pk>/add_schedule/', views.add_schedule, name='add_schedule'),
    path('subject/create/', views.create_subject, name='create_subject'),
    path('subject/<int:pk>/', views.subject_detail, name='subject_detail'),
    path('subject/<int:pk>/add_assignment/', views.add_assignment, name='add_assignment'),
    path('schedule/', views.schedule_page, name='schedule_page'),
    path('deadlines/', views.deadlines_page, name='deadlines_page'),
    path('submit/<int:id>/', views.submit_assignment, name='submit_assignment'),
]