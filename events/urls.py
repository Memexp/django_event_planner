from django.urls import path
from events import views
from api.views import (
    UpcomingEventListView,
    EventDetailView,
    EventUpdateView,
    EventCreateView,
    EventDeleteView,
    RegisterView,
    BookingView,
)
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
	path('', views.home, name='home'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('list/', views.event_list, name='event-list'),
    path('detail/<int:event_id>/', views.event_detail, name='event-detail'),
    path('create/', views.event_create, name='create-event'),
    path('update/<int:event_id>/', views.event_update, name='event-update'),
    path('delete/<int:event_id>/', views.event_delete, name='event-delete'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('profile/update/', views.update_profile, name='update-profile'),
    path('profile/<username>', views.user_profile, name='profile'),
    path('<int:user_id>/follow/',views.user_follow ,name='user-follow'),
    path('api/list/', UpcomingEventListView.as_view(), name='api-list'),
    path('api/create/', EventCreateView.as_view(), name='api-create'),
    path('api/login/', obtain_jwt_token, name='api-login'),
    path('api/<int:event_id>/detail/', EventDetailView.as_view(), name='api-detail'),
    path('api/<int:event_id>/book/', BookingView.as_view(), name='api-book'),
    path('api/<int:event_id>/update/', EventUpdateView.as_view(), name='api-update'),
    path('api/<int:event_id>/delete/', EventDeleteView.as_view(), name='api-delete'),
    path('api/register/', RegisterView.as_view(), name='api-register'),
]