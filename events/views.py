from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, EventForm, SeatForm
from .models import Event, Booking, Follow
from django.http import Http404, JsonResponse
from django.db.models import Q
from django.contrib import messages
from datetime import timedelta, datetime
from django.utils import timezone
from django.contrib.auth.models import User
# e-mail
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    events = Event.objects.filter(datetime__gte=datetime.today(),)[:10]

    context = {
        'events': events,
    }
    return render(request, 'home.html', context)

class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                if (request.user.event.all().exists()) :
                    return redirect('dashboard')
                else:
                    return redirect('event-list')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")

def user_profile(request, username):
    user = User.objects.get(username=username)

    events_list= Event.objects.filter(added_by__username=username)

    follow_obj= Follow.objects.filter(f=request.user).values_list('following', flat=True)

    f1= Follow.objects.filter(following=user).values_list('following', flat=True)
    f2= Follow.objects.filter(f=user).values_list('f', flat=True)

    print(follow_obj)
    context = {
        'events': events_list,
        'user': user,
        'follow_obj':follow_obj,
        'follower': f1,
        'following': f2,
    }
    return render(request, 'user_profile.html', context)


def update_profile(request):

    form = UserSignup(instance=request.user)

    if request.method == 'POST':
        form = UserSignup(request.POST, instance=request.user)
            
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "Updated Successfully.")
            login(request, user)
            return redirect("home")
        else:
            form = UserSignup(request.POST, instance=request.user)

    context = {
        'form':form,
    }
    return render(request, 'update_profile.html', context)



def event_list(request):
    if request.user.is_anonymous:
       return redirect('login')
    events = Event.objects.filter(datetime__gte=datetime.today(), )
    query = request.GET.get('q')
    if query:
        events = events.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(added_by__username__icontains=query)
        ).distinct()
    context = {
       'events': events,
    }

    return render(request, 'event_list.html', context)

def event_detail(request, event_id):
    event = Event.objects.get(id= event_id)

    form = SeatForm()
    if request.method == 'POST':
        form = SeatForm(request.POST)
        if event.seats_left() == 0:
            messages.warning(request, "No tickets left, please book another event, thank you.")
            return redirect('event-list')
        
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.event = event

            # checks if the tickets that the user want is greater than the seats left
            if booking.tickets > booking.event.seats_left():
                messages.warning(request, "The number of tickets exceeded the limit! enter a valid number please.")
                return redirect(event)
            
            # Sending a confirmation email to the user who booked
            subject = 'Booking Confirmation'
            message = ' Hi %s, \n\nthis is an email confirmation for you booking in our site. \nThank you. ' % (request.user.username)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email,]
            send_mail( subject, message, email_from, recipient_list )

            booking.save()
            return redirect('event-list')

    attendance = Event.ticket_sum(event)

    context = {
        'events': event,
        'form': form,
    }

    return render(request, 'event_detail.html', context)


def event_create(request):
    if request.user.is_anonymous:
        return redirect("login")
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST,request.FILES or None)
        if form.is_valid():
            event = form.save(commit=False)
            event.added_by = request.user
            event.save()
            
            # Email the followers 
            subject = 'HIIIIIIIIIIIIIIIIII'
            message = ' Testing the testing' 
            email_from = settings.EMAIL_HOST_USER
            print(event.added_by.following.values_list('f__email', flat=True))
            send_mail(
                subject,
                message,
                email_from,
                event.added_by.following.values_list('f__email', flat=True) , 
                fail_silently=False
                )

            return redirect('event-list')
    context = {
        'form': form,
    }
    return render(request,'create.html', context)

def event_update(request, event_id):

    event = Event.objects.get(id= event_id)

    if request.user.is_anonymous:
        return redirect('event-list')
    if not(request.user.is_staff or request.user == event.added_by):
        raise Http404

    form = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST,request.FILES, instance=event)
        if form.is_valid(): 
            form.save()
            # messages.success(request, "Successfully Updated!")
            return redirect('event-list')

    context = {
        'form': form,
        'event': event,
    }
    return render(request,'event_update.html', context)


def event_delete(request, event_id):
    Event.objects.get(id= event_id).delete()

    return redirect('event-list')


def user_dashboard(request):
    if request.user.is_anonymous:
        return redirect('login')

    events_list= Event.objects.filter(added_by=request.user)

    previous_events= Booking.objects.filter(user= request.user)

    
    context = {
        "events": events_list,
        'previous_events': previous_events,
    }
    return render(request, 'dashboard_events.html', context)


def user_follow(request, user_id):
    user_obj= User.objects.get(id= user_id)
    if request.user.is_anonymous:
        return redirect('signin')
    follow_obj, created = Follow.objects.get_or_create(following=user_obj, f=request.user)

    

    if created:
        follow='follow'
    else:
        follow='unfollow'
        follow_obj.delete()

    following_count= user_obj.following.all().count()
    follower_count= user_obj.follower.all().count()

    response = {
        'follow':follow,
        'following_count': follower_count,
        'follower_count': following_count,
    }
    return JsonResponse(response, safe=False)
















