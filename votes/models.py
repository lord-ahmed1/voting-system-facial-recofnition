from django.db import models


class VotesCollection(models.Model):
    title=models.CharField(max_length=200)
    candidates=models.CharField(max_length=200)
    
class VotesAndVoters(models.Model):
    vote_title=models.CharField(max_length=200)
    voter_username=models.CharField(max_length=200)
    
class Checker(models.Model):
    img=models.ImageField(default='default.jpg', upload_to='check')
# Create your models here.
