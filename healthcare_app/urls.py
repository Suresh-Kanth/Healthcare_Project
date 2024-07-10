from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.user_login, name='login'),
    # path('patient/', views.patient, name='patient'),
    # path('doctor/', views.doctor, name='doctor'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('logout/',views.Logout,name='logout'),
    path('addblog/',views.Add_Blog,name='addblog'),
    # path('blog/',views.blog,name='blog'),
    path('blogs/',views.blogs,name='blogs'),
    path('myblogs/',views.myblogs,name='myblogs'),
    path('mydrafts/',views.mydrafts,name='mydrafts'),
    path('blog/<uuid:blog_no>/', views.blog, name='blog'),
    path('draft/<uuid:blog_no>/', views.draft, name='draft'),
    path('bookappointment',views.bookappointment,name='bookappointment'),
    path('doctor_appointment/<uuid:doctor_no>/', views.doctor_appointment, name='doctor_appointment'),
    path('appointment_confirmation/<uuid:appointment_no>/', views.appointment_confirmation, name='appointment_confirmation'),
    path('myappointments/',views.myappointments,name='myappointments')
]
