from django.urls import path
from . import views



urlpatterns = [
    path('',views.index, name='index'),

    path('popular-courses/', views.popular_courses, name='popular_courses'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    path('team/', views.team, name='team'),
    path('team-details/<int:id>', views.team_details, name='team-details'),
    path('about/', views.about, name='about'),
    path('lecture/<int:id>', views.lecture, name='lecture'),
    path('find-program', views.find_program, name='find-program'),
    path('program-details/<int:id>', views.program_details, name='program-details'),


    path('course-details/<int:id>', views.course_details, name='course-details'),
    path('course-details-v2/<int:id>', views.course_details_v2, name='course-details-v2'),
    path('blog-details/<int:id>', views.blog_details, name='blog-details'),


    path('event-details/<int:id>', views.event_details, name='event-details'),
    path('become-tutor', views.become_tutor, name='become-tutor'),

    path('clear-course-item', views.clear_course_item, name='clear-course-item'),

    # API endpoints
    path('api/course/<int:id>/', views.course_detail, name='course_detail'),

    
]