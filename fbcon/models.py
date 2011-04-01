from django.db import models

class Movie(models.Model):
	pass 

	
class User(models.Model):
	username = models.CharField(max_length=128)
	first_name = models.CharField(max_length=128)
	last_name = models.CharField(max_length=128)
	gender = models.CharField(max_length=16)
	uid = models.IntegerField()
	hometown = models.CharField(max_length=2048)
	languages = models.CharField(max_length=2048)
	link = models.CharField(max_length=128)
	interested_in = models.CharField(max_length=1024)
	relationship_status = models.CharField(max_length=1024)
	religion = models.CharField(max_length=1024)
	photo_url = models.CharField(max_length=1024)
	
	#json encoded strings
	friends = models.TextField()
	movies = models.TextField()
	
	
