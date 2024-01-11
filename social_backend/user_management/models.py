from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime

class BaseModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

	@classmethod
	def to_date_time(self,timestamp):
		return datetime.fromtimestamp(timestamp)

	@classmethod
	def to_timestamp(self, time):
		return datetime.timestamp(time)
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    friends_list = models.ManyToManyField('self', symmetrical=True, blank=True)



class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    accepted = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('sender', 'receiver')

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'friend')

class FriendRequestLimit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_limits')
    requests_count = models.PositiveIntegerField(default=0)
    last_request_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'last_request_time')
