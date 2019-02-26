from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Event(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    date = models.DateField()
    starting_time = models.TimeField()
    ending_time = models.TimeField()
    # datetime = models.DateTimeField()
    img = models.ImageField(null=True, blank= True)
    added_by= models.ForeignKey(User, on_delete=models.CASCADE, related_name='event')
    seats = models.IntegerField()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'event_id': self.id})

    def update_url(self):
        return reverse('event-update', kwargs={'event_id': self.id})

    def ticket_sum(self):
        return sum([attends.tickets for attends in self.attends.all()])

    def seats_left(self):
        return self.seats - self.ticket_sum()

    

class Dashbord(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        pass
    
class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attends')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attends')
    tickets = models.IntegerField()

    def __str__(self):
        return self.event.title


        