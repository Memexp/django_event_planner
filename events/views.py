from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, EventForm, SeatForm
from .models import Event, Dashbord, Attend
from django.http import Http404, JsonResponse
from django.db.models import Q
from django.contrib import messages



def home(request):
    return render(request, 'home.html')

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
                return redirect('dashboard')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")

def event_list(request):
    event = Event.objects.all()

    context = {
        'events': event,
    }

    return render(request, 'event_list.html', context)

def event_detail(request, event_id):
    event = Event.objects.get(id= event_id)

    context = {
        'events': event,
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
    
    context = {
        "events": events_list,
    }
    return render(request, 'dashboard_events.html', context)

def seat_count(request, event_id):
    if request.user.is_anonymous:
        return redirect('signin')

    event_obj = Event.objects.get(id=event_id)

    form = SeatForm()
    if request.method == 'POST':
        form = SeatForm(request.POST)
        if form.is_valid():
            eve = form.save(commit=False)
            eve.user = request.user
            eve.event = event_obj
            eve.save()
            return redirect('event-list')
    
    attendance = Attend.seats_sum(Attend)

    print(attendance)


    if attendance != 0 and event_obj.seats > attendance :
        event_obj.seats = event_obj.seats - attendance

    event_obj.save()

    context = {
        'event_obj': event_obj,
        'form': form,
        'event_count': event_obj.seats,
    }
    return render(request, 'seat_count.html', context)
















