from django.db import models

class User(models.Model) :
	username = models.CharField(max_length = 15)
	password = models.CharField(max_length = 25)
	firstname = models.CharField(max_length = 25)
	lastname = models.CharField(max_length = 25)

class Blog(models.Model) :
	blogID = models.PositiveIntegerField()
	username = models.CharField(max_length = 15)			# owner of the blog
	title = models.CharField(max_length = 30)
	body = models.TextField()
	date = models.DateField()

class SessionList(models.Model) :
	key = models.CharField(max_length = 100)
	username = models.CharField(max_length = 25)