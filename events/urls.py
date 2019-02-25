from django.urls import path
from events import views

urlpatterns = [
	path('', views.home, name='home'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('list/', views.event_list, name='event-list'),
    path('detail/<int: event_id>/', views.event_detail, name='event-detail'),
]