from django.db import models

class Event(models.Model):
	title = models.CharField(max_length=40)
	description = models.TextField()
	date = models.DateField()
	starting_time = models.TimeField()
	ending_time = models.TimeField()


	def __str__(self):
		return self.title
